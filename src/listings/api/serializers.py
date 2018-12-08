from rest_framework import serializers

from listings.models import Listing

from realtors.serializers import RealtorSerializer


class ListingSerializer(serializers.ModelSerializer):
    realtor = RealtorSerializer()

    class Meta:
        model = Listing
        fields = "__all__"
