from rest_framework import serializers
from .models import PredictionHistory, DiseaseInfo


class PredictionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionHistory
        fields = [
            'id',
            'image',
            'predicted_disease',
            'confidence',
            'plant_type',
            'fertilizer_recommendation',
            'treatment_recommendation',
            'timestamp',
        ]
        read_only_fields = ['id', 'timestamp']


class DiseaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseInfo
        fields = [
            'id',
            'disease_name',
            'description',
            'symptoms',
            'causes',
            'prevention',
            'treatment',
            'fertilizer',
        ]
        read_only_fields = ['id']

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()