from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from listings.choices import state_choices, bedroom_choices, price_choices
from .models import Listing
from realtors.models import Realtor


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


@login_required
def submit_listing(request):
    if request.method == 'POST':
        # Get form data
        title = request.POST.get('title')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        description = request.POST.get('description')
        price = request.POST.get('price')
        bedrooms = request.POST.get('bedrooms')
        bathrooms = request.POST.get('bathrooms')
        garage = request.POST.get('garage')
        sqft = request.POST.get('sqft')
        lot_size = request.POST.get('lot_size')
        photo_main = request.FILES.get('photo_main')
        photo_1 = request.FILES.get('photo_1')
        photo_2 = request.FILES.get('photo_2')
        photo_3 = request.FILES.get('photo_3')
        photo_4 = request.FILES.get('photo_4')
        photo_5 = request.FILES.get('photo_5')
        photo_6 = request.FILES.get('photo_6')
        
        # Get the first available realtor (in a real app, you might assign based on location or availability)
        try:
            realtor = Realtor.objects.first()
            if not realtor:
                messages.error(request, 'No realtors available at the moment. Please contact us directly.')
                return render(request, 'listings/submit_listing.html', get_submit_context())
        except Exception as e:
            messages.error(request, 'There was an error processing your submission. Please try again.')
            return render(request, 'listings/submit_listing.html', get_submit_context())
        
        # Create new listing (initially unpublished for review)
        try:
            listing = Listing.objects.create(
                realtor=realtor,
                title=title,
                address=address,
                city=city,
                state=state,
                zipcode=zipcode,
                description=description,
                price=int(price) if price else 0,
                bedrooms=int(bedrooms) if bedrooms else 0,
                bathrooms=float(bathrooms) if bathrooms else 0,
                garage=int(garage) if garage else 0,
                sqft=int(sqft) if sqft else 0,
                lot_size=float(lot_size) if lot_size else 0,
                photo_main=photo_main,
                photo_1=photo_1,
                photo_2=photo_2,
                photo_3=photo_3,
                photo_4=photo_4,
                photo_5=photo_5,
                photo_6=photo_6,
                is_published=False  # Require admin approval
            )
            
            messages.success(request, 'Your property has been submitted successfully! It will be reviewed by our team and published within 24 hours.')
            return redirect('listings:listings')
            
        except Exception as e:
            messages.error(request, 'There was an error submitting your property. Please check all fields and try again.')
            return render(request, 'listings/submit_listing.html', get_submit_context())
    
    # GET request - show the form
    return render(request, 'listings/submit_listing.html', get_submit_context())


def get_submit_context():
    """Helper function to get context for submit listing form"""
    return {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
    }
