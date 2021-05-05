import base64
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
            facilities_list = []

            if 'image_id_list' in data:
                list_of_image_ids = data['image_id_list']
                if len(list_of_image_ids) > 0:
                    for id in list_of_image_ids:
                        try:
                            image_to_add = Image.objects.get(image_id=id)
                            images_to_add.append(image_to_add)
                        except Image.DoesNotExist:
                            return Response(f"Image with image_id {id} NOT FOUND!", status=status.HTTP_404_NOT_FOUND)

            if 'doc_id_list' in data:
                list_of_doc_ids = data['doc_id_list']
                if len(list_of_doc_ids) > 0:
                    for id in list_of_doc_ids:
                        try:
                            doc_to_add = Document.objects.get(document_id=id)
                            documents_to_add.append(doc_to_add)
                        except Document.DoesNotExist:
                            return Response(f"Document with document_id {id} NOT FOUND!",
                                            status=status.HTTP_404_NOT_FOUND)

            if 'facilities_list' in data:
                for facility in data['facilities_list']:
                    facility_obj, created = Facility.objects.get_or_create(name=facility)
                    facilities_list.append(facility_obj)
            else:
                return Response(f"Facilities_list: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

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

        for facility in facilities_list:
            villa.facilities.add(facility)

        # if 'filename' in request.data and 'image' in request.data:
        #     filename = request.data['filename']
        #     file = ContentFile(base64.b64decode(request.data['image']), name=filename)
        #     account.image = file

        villa.save()

        return Response(f"Villa with villa_id {villa.villa_id} created successfully!",
                        status=status.HTTP_201_CREATED)

@api_view(['GET', ])
def search(request):
    query = Q()
    data = request.GET
    if 'country' in data.keys():
        query = query & Q(country=data['country'])

    if 'city' in data.keys():
        query = query & Q(city=data['city'])    

    villas = Villa.objects.filter(query)
    serializer = VillaSerializer(data=villas, many=True)
    serializer.is_valid()
    return Response({"message":'search successfully' , "data" : serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET', ])
def show_villa_calendar(request):
    try:
        villa = Villa.objects.get(villa_id=request.GET['villa_id'])
    except:
        return Response({'message':'villa does not exist'}, status=status.HTTP_404_NOT_FOUND)
    dates = Calendar.objects.filter(villa=villa)
    serializer = ShowVillaCalendarSerializer(data=dates, many=True)
    serializer.is_valid()
    data = serializer.data
    return Response({'message':'show villa calendar successfully', 'dates':data}, status=status.HTTP_200_OK)