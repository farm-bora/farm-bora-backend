from rest_framework import serializers
from .models import Plant, Disease


class NestedDiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = ("id", "name", "details")


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = ("id", "name", "details", "plant")


class PlantSerializer(serializers.ModelSerializer):
    diseases = NestedDiseaseSerializer(many=True, read_only=True)

    class Meta:
        model = Plant
        fields = ("id", "name", "botanical_name", "details", "image", "diseases")


class PlantDiseaseSearchSerializer(serializers.Serializer):
    image_base64 = serializers.CharField()
