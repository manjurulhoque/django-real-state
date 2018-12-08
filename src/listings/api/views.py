from django.http import JsonResponse
from rest_framework import status, filters
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404

from listings.api.serializers import ListingSerializer

from listings.models import Listing
from rest_framework.response import Response


class ListingsListApiView(ListAPIView):
    serializer_class = ListingSerializer
    model = serializer_class.Meta.model
    # paginate_by_param = 'page'
    queryset = model.objects.order_by('-list_date').filter(is_published=True)

    # def get_queryset(self):
    #     return self.model.objects.order_by('-list_date').filter(is_published=True)


class ListingDetailView(RetrieveAPIView):
    serializer_class = ListingSerializer
    model = serializer_class.Meta.model
    lookup_url_kwarg = 'listing_id'
    queryset = Listing.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        return obj


class SearchView(ListAPIView):
    serializer_class = ListingSerializer
    model = serializer_class.Meta.model

    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('city', 'description', 'state', 'price')

    def get_queryset(self):
        queryset_list = self.model.objects.all()

        # Keywords
        if 'keywords' in self.request.GET:
            keywords = self.request.GET['keywords']
            if keywords:
                queryset_list = queryset_list.filter(description__icontains=keywords)

        # City
        if 'city' in self.request.GET:
            city = self.request.GET['city']
            if city:
                queryset_list = queryset_list.filter(city__iexact=city)

        # State
        if 'state' in self.request.GET:
            state = self.request.GET['state']
            if state:
                queryset_list = queryset_list.filter(state__iexact=state)

        # Bedrooms
        if 'bedrooms' in self.request.GET:
            bedrooms = self.request.GET['bedrooms']
            if bedrooms:
                queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

        # Price
        if 'price' in self.request.GET:
            price = self.request.GET['price']
            if price:
                queryset_list = queryset_list.filter(price__lte=price)

        return queryset_list
