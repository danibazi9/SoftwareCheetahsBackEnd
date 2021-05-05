from rest_framework import serializers
from villa.models import *


class VillaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Villa
        fields = '__all__'


class RuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rule
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = '__all__'
