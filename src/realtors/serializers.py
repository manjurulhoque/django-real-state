from rest_framework import serializers

from realtors.models import Realtor


class RealtorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Realtor
        fields = "__all__"
