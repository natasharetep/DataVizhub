from rest_framework import serializers
from .models import DataFile

class DataFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataFile
        fields = ['file', 'uploaded_at']


    def create(self, validated_data):
        return DataFile.objects.create(**validated_data)

