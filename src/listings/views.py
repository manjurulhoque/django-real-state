from django.shortcuts import render
from django.views.generic import ListView, DetailView

from listings.choices import state_choices, bedroom_choices, price_choices
from .models import Listing


# Create your views here.
class ListingsListView(ListView):
    model = Listing
    template_name = 'listings/listings.html'
    queryset = Listing.objects.order_by('-list_date').filter(is_published=True)
    context_object_name = 'listings'
    paginate_by = 2


# def index(request):
#     return render(request, 'listings/listings.html')

class ListingDetailView(DetailView):
    model = Listing
    template_name = 'listings/listing.html'
    context_object_name = 'listing'
    pk_url_kwarg = 'listing_id'

#
# def listing(request):
#     return render(request, 'listings/listing.html')


def search(request):
    queryset_list = Listing.objects.all()

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

    # City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    # State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values': request.GET
    }

    return render(request, 'listings/search.html', context)
