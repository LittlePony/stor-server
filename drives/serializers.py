from rest_framework import serializers


class PartitionSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    size = serializers.CharField(max_length=10)
    mountpoint = serializers.CharField(max_length=500)
    type = serializers.CharField(max_length=5)


class DriveSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    size = serializers.CharField(max_length=10)
    mountpoint = serializers.CharField(max_length=500)
    children = PartitionSerializer(many=True, read_only=True)
    type = serializers.CharField(max_length=5)
