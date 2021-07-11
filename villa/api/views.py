import base64
import datetime
import json

from django.core.files.base import ContentFile
from push_notifications.models import GCMDevice
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.db.models import Count

from villa.api.serializer import *
from villa.models import *


def add_additional_info(villa_data, user_id):
    final_data = villa_data

    for x in final_data:
        owner = Account.objects.get(user_id=x['owner'])
        x['owner'] = owner.__str__()
        x['owner_image'] = None

        if owner.image:
            x['owner_image'] = owner.image.url

        facilities_list = []

        for facility_id in x['facilities']:
            facility = Facility.objects.get(facility_id=facility_id)
            facilities_list.append(facility.name)
        x['facilities'] = facilities_list

        images_list = []

        for image_id in x['images']:
            image = Image.objects.get(image_id=image_id)
            images_list.append(image.image.url)
        x['images'] = images_list

        documents_list = []

        for document_id in x['documents']:
            document = Document.objects.get(document_id=document_id)
            documents_list.append(document.file.url)
        x['documents'] = documents_list

        rules_list = []

        for rule_id in x['rules']:
            rule = Rule.objects.get(rule_id=rule_id)
            rules_list.append(rule.text)
        x['rules'] = rules_list

        if user_id in x['likes']:
            x['like'] = True
        else:
            x['like'] = False

        del x['likes']

        try:
            Calendar.objects.get(villa__villa_id=x['villa_id'], customer__user_id=owner.user_id,
                                 end_date__gte=datetime.datetime.now().date())
            x['reserved'] = True
        except Calendar.DoesNotExist:
            x['reserved'] = False

    return final_data


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_user_villas(request):
    hosted = request.query_params.get('hosted', None)
    reserved = request.query_params.get('reserved', None)

    if hosted is not None and reserved is None:
        villas = Villa.objects.filter(owner=request.user)

        serializer = VillaSerializer(villas, many=True)
        data = json.loads(json.dumps(serializer.data))
    elif reserved is not None and hosted is None:
        reserved_rows = Calendar.objects.filter(
            customer__user_id=request.user.user_id,
            end_date__gte=datetime.datetime.now().date()
        )

        serializer = MyCalendarSerializer(reserved_rows, many=True)
        data = json.loads(json.dumps(serializer.data))

        for x in data:
            for key in x['villa'].keys():
                x[key] = x['villa'][key]
            del x['villa']

            x['reserved_dates'] = f"{str(x['start_date'])},{str(x['end_date'])}"
            del x['start_date']
            del x['end_date']
    else:
        return Response("hosted/reserved: BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

    return Response({'data': add_additional_info(data, request.user.user_id)}, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_all_villas(request):
    all_villas = Villa.objects.filter(visible=True)

    serializer = VillaSerializer(all_villas, many=True)
    data = json.loads(json.dumps(serializer.data))

    return Response({'data': add_additional_info(data, request.user.user_id)}, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def upload_image(request):
    if 'file' in request.data.keys():
        new_data = request.data
        new_data['image'] = request.data['file']
        new_data['file'] = None
        serializer = ImageSerializer(data=new_data)
    else:
        if 'filename' in request.data and 'image_file' in request.data:
            try:
                filename = request.data['filename']
                file = ContentFile(base64.b64decode(request.data['image_file']), name=filename)
                new_image = Image.objects.create(image=file)
                serializer = ImageSerializer(new_image)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(f"ERROR: {e}", status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def upload_document(request):
    serializer = DocumentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class UserVilla(APIView):
    def get(self, args):
        villa_id = self.request.query_params.get('villa_id', None)
        if villa_id is not None:
            try:
                villa = Villa.objects.get(villa_id=villa_id)
            except Villa.DoesNotExist:
                return Response(f"Villa with villa_id {villa_id} NOT FOUND!", status=status.HTTP_404_NOT_FOUND)

            serializer = VillaSerializer(villa)
            data = json.loads(json.dumps(serializer.data))

            owner = Account.objects.get(user_id=data['owner'])
            data['owner'] = owner.__str__()
            data['owner_id'] = owner.user_id
            data['phone_number'] = owner.phone_number
            data['owner_image'] = None

            if owner.image:
                data['owner_image'] = owner.image.url

            visible = self.request.query_params.get('visible', None)
            if visible is not None:
                if visible == 'true':
                    villa.visible = True
                elif visible == 'false':
                    villa.visible = False
                else:
                    return Response("Visible: BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

            villa.save()

            facilities_list = []

            for facility_id in data['facilities']:
                facility = Facility.objects.get(facility_id=facility_id)
                facilities_list.append(facility.name)
            data['facilities'] = facilities_list

            images_list = []

            for image_id in data['images']:
                image = Image.objects.get(image_id=image_id)
                images_list.append(image.image.url)
            data['images'] = images_list

            documents_list = []

            for document_id in data['documents']:
                document = Document.objects.get(document_id=document_id)
                documents_list.append(document.file.url)
            data['documents'] = documents_list

            rules_list = []

            for rule_id in data['rules']:
                rule = Rule.objects.get(rule_id=rule_id)
                rules_list.append(rule.text)
            data['rules'] = rules_list

            if self.request.user.user_id in data['likes']:
                data['like'] = True
            else:
                data['like'] = False

            del data['likes']

            reserved_rows = Calendar.objects.filter(villa__villa_id=villa_id,
                                                    customer__user_id=self.request.user.user_id,
                                                    end_date__gte=datetime.datetime.now().date())

            if len(reserved_rows) != 0:
                data['reserved'] = True
            else:
                data['reserved'] = False

            data['user_id'] = self.request.user.user_id

            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response("Villa_id: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def post(self, args):
        data = json.loads(json.dumps(self.request.data))
        data['owner'] = self.request.user.user_id

        serializer = VillaSerializer(data=data)
        if serializer.is_valid():
            images_to_add = []
            documents_to_add = []
            rules_to_add = []
            facilities_list = []

            if 'image_id_list' in data:
                list_of_image_ids = data['image_id_list']
                if len(list_of_image_ids) > 0:
                    for image_id in list_of_image_ids:
                        try:
                            image_to_add = Image.objects.get(image_id=image_id)
                            images_to_add.append(image_to_add)
                        except Image.DoesNotExist:
                            return Response(f"Image with image_id {image_id} NOT FOUND!",
                                            status=status.HTTP_404_NOT_FOUND)

            if 'doc_id_list' in data:
                list_of_doc_ids = data['doc_id_list']
                if len(list_of_doc_ids) > 0:
                    for doc_id in list_of_doc_ids:
                        try:
                            doc_to_add = Document.objects.get(document_id=doc_id)
                            documents_to_add.append(doc_to_add)
                        except Document.DoesNotExist:
                            return Response(f"Document with document_id {doc_id} NOT FOUND!",
                                            status=status.HTTP_404_NOT_FOUND)

            if 'facilities_list' in data:
                for facility in data['facilities_list']:
                    facility_obj, created = Facility.objects.get_or_create(name=facility)
                    facilities_list.append(facility_obj)
            else:
                return Response(f"Facilities_list: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

            if 'rule_id_list' in data:
                list_of_rule_ids = data['rule_id_list']
                if len(list_of_rule_ids) > 0:
                    for rule_id in list_of_rule_ids:
                        try:
                            rule_to_add = Rule.objects.get(rule_id=rule_id)
                            rules_to_add.append(rule_to_add)
                        except Rule.DoesNotExist:
                            return Response(f"Rule with rule_id {rule_id} NOT FOUND!",
                                            status=status.HTTP_404_NOT_FOUND)

            villa = serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if 'description' in data:
            villa.description = data['description']

        if 'number_of_bathrooms' in data:
            villa.number_of_bathrooms = int(data['number_of_bathrooms'])

        if 'number_of_bedrooms' in data:
            villa.number_of_bedrooms = int(data['number_of_bedrooms'])

        if 'number_of_single_beds' in data:
            villa.number_of_single_beds = int(data['number_of_single_beds'])

        if 'number_of_double_beds' in data:
            villa.number_of_double_beds = int(data['number_of_double_beds'])

        if 'number_of_showers' in data:
            villa.number_of_showers = int(data['number_of_showers'])

        default_image = images_to_add[0]
        default_image.default = True
        default_image.save()

        for image in images_to_add:
            villa.images.add(image)

        for document in documents_to_add:
            villa.documents.add(document)

        for rule in rules_to_add:
            villa.rules.add(rule)

        for facility in facilities_list:
            villa.facilities.add(facility)

        villa.save()

        try:
            fcm_devices = GCMDevice.objects.all().exclude(user=self.request.user)
            for device in fcm_devices:
                device.send_message(title=f"Hey, We've got a new villa for you!",
                                    message=f"{villa.country}, {villa.state}, {villa.city}"
                                    )
        except Exception as e:
            print(f"Error: {e}")

        return Response(f"Villa with villa_id {villa.villa_id} created successfully!",
                        status=status.HTTP_201_CREATED)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_fixed_rules(request):
    fixed_rules = [
        '3 days ahead of schedule nothing will be returned.',
        '7 days ahead of schedule 30% of price will be returned.',
        'More than 7 days ahead of schedule 100% of price will be returned.'
    ]

    data = json.loads(json.dumps(fixed_rules))
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_special_rules(request):
    special_rules = [
        'Smoking is not allowed in this place.',
        'Pets are not allowed in this villa.',
        'You can not invite more people than the maximum capacity.',
        'We have no responsibility for lost property.',
        'This place is rented only to the family.',
        'In case of damage to the place, you will be compensated.',
        'You are only allowed to park a car in the parking lot.',
        'You are not allowed to put garbage in the yard or in the alley and it should be put in the trash.',
        'The responsibility of cleaning the place is with you and no one is intended for this action.'
    ]

    for special_rule in special_rules:
        Rule.objects.get_or_create(text=special_rule)

    all_special_rules = Rule.objects.all()
    serializer = RuleSerializer(all_special_rules, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', ])
def search(request):
    query = Q()
    data = request.GET
    if 'country' in data.keys():
        query = query & Q(country=data['country'])

    if 'city' in data.keys():
        query = query & Q(city=data['city'])

    if 'state' in data.keys():
        query = query & Q(state=data['state'])

    villas = Villa.objects.filter(query)
    if 'start_date' in data.keys() and 'end_date' in data.keys():
        start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d')
        end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d')
        selected_villas = []
        for v in villas:
            query = Q(villa=v)
            query = query & (
                    Q(start_date__gte=start_date.date(), start_date__lt=end_date.date())
                    | Q(start_date__lte=start_date.date(), end_date__gte=end_date.date())
                    | Q(end_date__gt=start_date.date(), end_date__lte=end_date.date())
            )
            no_overlapped_calendars = Calendar.objects.filter(query).count()
            if no_overlapped_calendars == 0:
                selected_villas.append(v)
    else:
        selected_villas = villas
    serializer = VillaSearchSerializer(data=selected_villas, many=True)
    serializer.is_valid()
    len_data = len(serializer.data)
    if int(data['number_of_villa']) < len_data:
        start = (int(data['page']) - 1) * int(data['number_of_villa'])
        end = min(int(data['page']) * int(data['number_of_villa']), len_data)
        return Response({"message": 'search successfully', "data": serializer.data[start:end]},
                        status=status.HTTP_200_OK)
    else:
        return Response({"message": 'search successfully', "data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def show_villa_calendar(request):
    try:
        villa = Villa.objects.get(villa_id=request.GET['villa_id'])
    except Villa.DoesNotExist:
        return Response({'message': 'villa does not exist'}, status=status.HTTP_404_NOT_FOUND)
    dates = Calendar.objects.filter(villa=villa)
    serializer = CalendarSerializer(data=dates, many=True)
    serializer.is_valid()
    data = serializer.data
    date_list = []
    for date in data:
        start_date = datetime.datetime.strptime(date['start_date'], '%Y-%m-%d')
        end_date = datetime.datetime.strptime(date['end_date'], '%Y-%m-%d')
        current_date = start_date
        while current_date <= end_date:
            date_list.append(current_date.strftime('%Y-%m-%d'))
            current_date = current_date + datetime.timedelta(days=1)

    return Response({'message': 'show villa calendar successfully', 'dates': date_list}, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def register_villa(request):
    data = json.loads(json.dumps(request.data))
    data['customer'] = request.user.user_id

    if 'start_date' not in request.data:
        return Response('Start_date: None, BAD REQUEST!', status=status.HTTP_400_BAD_REQUEST)

    if 'end_date' not in request.data:
        return Response('End_date: None, BAD REQUEST!', status=status.HTTP_400_BAD_REQUEST)

    start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d')
    end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d')

    if start_date.date() > end_date.date():
        return Response(f"ERROR: the start_date can't be larger than end_date!", status=status.HTTP_400_BAD_REQUEST)

    if start_date.date() < datetime.date.today():
        return Response(f"ERROR: the start_date can't be for the past!", status=status.HTTP_400_BAD_REQUEST)

    if end_date.date() < datetime.date.today():
        return Response(f"ERROR: the end_date can't be for the past!", status=status.HTTP_400_BAD_REQUEST)

    overlapped_calendars = Calendar.objects.filter(
        Q(start_date__gte=start_date.date(), start_date__lt=end_date.date())
        | Q(start_date__lte=start_date.date(), end_date__gte=end_date.date())
        | Q(end_date__gt=start_date.date(), end_date__lte=end_date.date())
    )
    if len(overlapped_calendars) > 0:
        return Response(f"ERROR: This period has overlapped with other registration!",
                        status=status.HTTP_400_BAD_REQUEST)

    serializer = RegisterVillaSerializer(data=data)
    if serializer.is_valid():
        villa = serializer.save()

        try:
            customer_device = GCMDevice.objects.get(user=request.user)
            host_device = GCMDevice.objects.get(user=villa.owner)

            customer_device.send_message(title=f"Reservation done!",
                                         message=f"The villa reserved for you between {start_date} - {end_date}"
                                         )

            host_device.send_message(title=f"Hey, you have a new guest!",
                                     message=f"A new customer reserved your villa between {start_date} - {end_date}"
                                     )
        except Exception as e:
            print(f"Error: {e}")

        return Response(f"Villa with villa_id {villa.villa_id} registered successfully!",
                        status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@permission_classes([])
def get_most_reserved_city(request):
    if 'number_of_city' not in request.GET:
        return Response(f"Number_of_city: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

    number_of_villa = int(request.GET['number_of_city'])

    query = Q()
    if 'country' in request.GET.keys():
        country = request.GET['country']
        query = query & Q(villa__country=country)
    if 'state' in request.GET.keys():
        state = request.GET['state']
        query = query & Q(villa__state=state)

    most_registered = Calendar.objects.filter(query).values('villa__country', 'villa__state',
                                                            'villa__city').order_by().annotate(
        Count('villa__city')).order_by('villa__city__count')[::-1][:number_of_villa]
    data_list = []
    for v in most_registered:
        data = {}
        villa_count = Villa.objects.filter(country=v['villa__country'], state=v['villa__state'],
                                           city=v['villa__city']).count()
        data['country'] = v['villa__country']
        data['state'] = v['villa__state']
        data['city'] = v['villa__city']
        data['no_villa'] = villa_count
        data_list.append(data)

    return Response({'message': 'show most popular city successfully', 'data': data_list}, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([])
def show_most_registered_villas(request):
    if 'number_of_villa' not in request.GET:
        return Response(f"Number_of_villa: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

    number_of_villa = int(request.GET['number_of_villa'])
    most_registered = Calendar.objects.values('villa').order_by().annotate(Count('villa')).order_by('villa__count')[
                      ::-1][:number_of_villa]

    data = []
    for v in most_registered:
        villa = Villa.objects.get(villa_id=v['villa'])
        serializer = VillaSearchSerializer(villa)
        data.append(serializer.data)
    return Response({'message': 'find most reserved successfully', 'data': data}, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([])
def show_most_rated_villas(request):
    if 'number_of_villa' not in request.GET:
        return Response(f"Number_of_villa: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

    number_of_villa = int(request.GET['number_of_villa'])
    most_rated = Villa.objects.filter(Q(no_rate__gt=0)).order_by('rate')[::-1][:number_of_villa]
    serializer = VillaSearchSerializer(many=True, data=most_rated)
    serializer.is_valid()
    return Response({'message': 'find most rated successfully', 'data': serializer.data},
                    status=status.HTTP_200_OK)


@api_view(['POST', ])
def add_rate(request):
    user = request.user

    if 'villa_id' not in request.data.keys():
        return Response({'message': 'villa_id field required'},
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            villa = Villa.objects.get(villa_id=request.data['villa_id'])
        except:
            return Response({'message': 'villa does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    if 'rate' in request.data.keys():
        reserve = Calendar.objects.filter(customer=user, villa=villa)
        if list(reserve) == []:
            return Response({'message': 'reserve does not exist'},
                            status=status.HTTP_404_NOT_FOUND)
        reserve = list(reserve)[-1]
        reserve.rate = int(request.POST['rate'])
        reserve.save()
        villa.rate = ((villa.rate * villa.no_rate) + reserve.rate) / (villa.no_rate + 1)
        villa.no_rate += 1
        villa.save()
        serializer = VillaSearchSerializer(villa)
        return Response({'message': 'add rate successfully', 'data': serializer.data},
                        status=status.HTTP_200_OK)
    else:
        return Response({'message': 'rate field required'},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
def cancel_reserve(request):
    if 'reserve_id' not in request.data.keys():
        return Response({'message': 'reserve_id field required'},
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            reserve = Calendar.objects.get(reserve_id=int(request.data['reserve_id']))
            reserve.delete()
            return Response({'message': 'cancel reserve successfully'},
                            status=status.HTTP_200_OK)
        except:
            return Response({'message': 'reserve does not exist'},
                            status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def like_villa(request):
    if 'villa_id' not in request.data:
        return Response("Villa_id: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

    if 'like' not in request.data:
        return Response("Like: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

    villa_id = request.data['villa_id']
    like = request.data['like']

    try:
        villa = Villa.objects.get(villa_id=villa_id)
    except Villa.DoesNotExist:
        return Response(f"Villa with villa_id {villa_id} doesn't exist!", status=status.HTTP_404_NOT_FOUND)

    if like == 'true':
        villa.likes.add(request.user)
        return Response("Successfully liked!", status=status.HTTP_200_OK)
    elif like == 'false':
        villa.likes.remove(request.user)
        return Response("Successfully disliked!", status=status.HTTP_200_OK)
    else:
        return Response("Like: BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_favourite_villas(request):
    favourite_villas = Villa.objects.filter(likes__user_id=request.user.user_id)

    serializer = VillaSerializer(favourite_villas, many=True)
    data = json.loads(json.dumps(serializer.data))

    return Response({'data': add_additional_info(data, request.user.user_id)}, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def check_postal_code(request):
    if 'postal_code' not in request.data:
        return Response("Postal_code: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

    postal_code = request.data['postal_code']

    try:
        Villa.objects.get(postal_code=postal_code)
        return Response("There exist a villa with this postal code!", status=status.HTTP_406_NOT_ACCEPTABLE)
    except Villa.DoesNotExist:
        return Response("There isn't any villa with this postal code!", status=status.HTTP_200_OK)
