from rest_framework import serializers
from .models import Plant


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ("id", "name", "botanical_name", "details", "image")


class PlantDiseaseSearchSerializer(serializers.Serializer):
    image_base64 = serializers.CharField()
