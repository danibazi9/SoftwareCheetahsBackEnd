import base64
import json

from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from villa.api.serializer import *
from villa.models import *


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_all_villas(request):
    all_villas = Villa.objects.all()

    serializer = VillaSerializer(all_villas, many=True)
    data = json.loads(json.dumps(serializer.data))

    for x in data:
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
        serializer = ImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def upload_document(request):
    data = request.data
    data['user'] = request.user.user_id

    serializer = DocumentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def check_document_existence(request):
    documents = Document.objects.filter(user=request.user)
    if len(documents) > 0:
        return Response('Document found successfully!', status=status.HTTP_200_OK)
    else:
        return Response('No document exist!', status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def remove_waste_images(request):
    images_to_remove = Image.objects.filter(villa=None)
    images_to_remove.delete()
    return Response("Waste images removed successfully!", status=status.HTTP_200_OK)


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

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("Villa_id: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)

    def post(self, args):
        data = json.loads(json.dumps(self.request.data))
        data['owner'] = self.request.user.user_id

        serializer = VillaSerializer(data=data)
        if serializer.is_valid():
            images_to_add = []
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

        for image in images_to_add:
            villa.images.add(image)

        for facility in facilities_list:
            villa.facilities.add(facility)

        # if 'filename' in request.data and 'image' in request.data:
        #     filename = request.data['filename']
        #     file = ContentFile(base64.b64decode(request.data['image']), name=filename)
        #     account.image = file

        villa.save()

        return Response(f"Villa with villa_id {villa.villa_id} created successfully!",
                        status=status.HTTP_201_CREATED)
