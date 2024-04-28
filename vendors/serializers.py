from rest_framework import serializers
from .models import *

class VendorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    contact_details = serializers.CharField()
    address = serializers.CharField()
    vendor_code = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return Vendor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.contact_details = validated_data.get('contact_details', instance.contact_details)
        instance.address = validated_data.get('address', instance.address)
        instance.vendor_code = validated_data.get('vendor_code', instance.vendor_code)
        instance.save()
        return instance
