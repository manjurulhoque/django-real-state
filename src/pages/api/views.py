from django.http import JsonResponse
from django.shortcuts import render, redirect

from listings.choices import state_choices, bedroom_choices, price_choices
from listings.models import Listing

from listings.api.serializers import ListingSerializer


def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True).select_related('realtor', )[:3]
    serializer = ListingSerializer(listings, many=True)
    listings = serializer.data

    context = {
        'listings': listings,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices
    }

    return JsonResponse(context)
