from rest_framework import serializers
from villa.models import *


class VillaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Villa
        fields = '__all__'

class VillaSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Villa
        fields = ['name', 'country', 'state', 'city', 'price_per_night', 'images']


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
