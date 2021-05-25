import base64
import datetime
import json

from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from villa.api.serializer import *
from villa.models import *


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_all_villas(request):
    all_villas = Villa.objects.filter(visible=True)

    my_flag = request.query_params.get('me', None)
    if my_flag is not None:
        all_villas = Villa.objects.filter(owner=request.user, visible=True)

    serializer = VillaSerializer(all_villas, many=True)
    data = json.loads(json.dumps(serializer.data))

    for x in data:
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

    return Response(data, status=status.HTTP_200_OK)


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
                    for id in list_of_rule_ids:
                        try:
                            rule_to_add = Rule.objects.get(rule_id=id)
                            rules_to_add.append(rule_to_add)
                        except Rule.DoesNotExist:
                            return Response(f"Rule with rule_id {id} NOT FOUND!",
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

        return Response(f"Villa with villa_id {villa.villa_id} created successfully!",
                        status=status.HTTP_201_CREATED)


@permission_classes((IsAuthenticated,))
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_fixed_rules(request):
    fixed_rules = [
        '3 days ahead of schedule nothing will be returned.',
        '7 days ahead of schedule 30 % of price will be returned.',
        'More than 7 days ahead of schedule 100 % of price will be returned.'
    ]

    data = json.loads(json.dumps(fixed_rules))
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_special_rules(request):
    special_rules = [
        'Not suitable for children',
        'Not suitable for infants',
        'No smoking',
        'No pets',
        'No parties or events'
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
    serializer = VillaSearchSerializer(data=villas, many=True)
    serializer.is_valid()
    len_data = len(serializer.data)
    if int(data['number_of_villa']) < len_data:
        start = (int(data['page']) - 1) * int(data['number_of_villa'])
        end = min(int(data['page']) * int(data['number_of_villa']), len_data)
        return Response({"message": 'search successfully', "data": serializer.data[start:end]}, status=status.HTTP_200_OK)
    else:
        return Response({"message": 'search successfully', "data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET', ])
def show_villa_calendar(request):
    try:
        villa = Villa.objects.get(villa_id=request.GET['villa_id'])
    except Villa.DoesNotExist:
        return Response({'message': 'villa does not exist'}, status=status.HTTP_404_NOT_FOUND)
    dates = Calendar.objects.filter(villa=villa)
    serializer = CalendarSerializer(data=dates, many=True)
    serializer.is_valid()
    data = serializer.data
    return Response({'message': 'show villa calendar successfully', 'dates': data}, status=status.HTTP_200_OK)


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

    serializer = CalendarSerializer(data=data)
    if serializer.is_valid():
        villa = serializer.save()
        return Response(f"Villa with villa_id {villa.villa_id} registered successfully!",
                        status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
