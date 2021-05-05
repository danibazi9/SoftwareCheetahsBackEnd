from rest_framework import serializers
from villa.models import *


class VillaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Villa
        fields = '__all__'

class VillaSearchSerializer(serializers.ModelSerializer):
    default_image_url = serializers.SerializerMethodField('get_default_image')

    class Meta:
        model = Villa
        fields = ['name', 'country', 'state', 'city', 'price_per_night', 'default_image_url']

    def get_default_image(self, villa):
        images = villa.images
        for i in images.all():
            if i.default:
                return i.image.url


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = '__all__'

class ShowVillaCalendarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Calendar
        fields = ['villa', 'start_date','end_date', 'closed']
