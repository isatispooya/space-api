from rest_framework import serializers
from .models import Correspondence, Attache
from positions.serializers import PositionSerializer


class AttacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attache
        fields = ['id', 'name', 'file']

        
class CorrespondenceSerializer(serializers.ModelSerializer):
    attache_details = AttacheSerializer(source='attache', read_only=True)
    attache_file = serializers.FileField(write_only=True, required=False)
    attache_name = serializers.CharField(write_only=True, required=False)
    sender = PositionSerializer(read_only=True)

    class Meta:
        model = Correspondence
        fields = '__all__'

    def create(self, validated_data):
        attache_file = validated_data.pop('attache_file', None)
        attache_name = validated_data.pop('attache_name', None)

        if attache_file and attache_name:
            attache = Attache.objects.create(
                name=attache_name,
                file=attache_file
            )
            validated_data['attache'] = attache

        return super().create(validated_data)



