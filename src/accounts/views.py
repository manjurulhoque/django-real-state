from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST


# Create your views here.
from contacts.models import Contact
from listings.models import Listing
from .models import UserProfile, Wishlist
from .forms import UserUpdateForm, UserProfileUpdateForm


def register(request):
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if passwords match
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used')
                    return redirect('register')
                else:
                    # Looks good
                    user = User.objects.create_user(username=username, password=password, email=email,
                                                    first_name=first_name, last_name=last_name)
                    # Login after register
                    # auth.login(request, user)
                    # messages.success(request, 'You are now logged in')
                    # return redirect('index')
                    user.save()
                    messages.success(request, 'You are now registered and can log in')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('accounts:register')
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('accounts:login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('pages:index')


@login_required
def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    user_listings = Listing.objects.order_by('-list_date').filter(submitted_by=request.user)
    user_wishlist = Wishlist.objects.filter(user=request.user).select_related('listing')

    context = {
        'contacts': user_contacts,
        'listings': user_listings,
        'wishlist_count': user_wishlist.count(),
    }
    
    # Add admin statistics if user is superuser
    if request.user.is_superuser:
        context.update({
            'total_listings': Listing.objects.count(),
            'published_count': Listing.objects.filter(is_published=True).count(),
            'unpublished_count': Listing.objects.filter(is_published=False).count(),
        })
    
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile_update(request):
    """View for updating user profile"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user.userprofile
        )
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile_update')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=request.user.userprofile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/profile_update.html', context)


@login_required
def wishlist(request):
    """View for displaying user's wishlist"""
    user_wishlist = Wishlist.objects.filter(user=request.user).select_related('listing').order_by('-added_at')
    
    # Pagination
    paginator = Paginator(user_wishlist, 6)  # Show 6 properties per page
    page = request.GET.get('page')
    wishlist_items = paginator.get_page(page)
    
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'accounts/wishlist.html', context)


@login_required
@require_POST
def add_to_wishlist(request, listing_id):
    """AJAX view for adding property to wishlist"""
    listing = get_object_or_404(Listing, id=listing_id, is_published=True)
    
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        listing=listing
    )
    
    if created:
        return JsonResponse({
            'success': True,
            'message': 'Property added to your wishlist!',
            'action': 'added'
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Property is already in your wishlist.',
            'action': 'exists'
        })


@login_required
@require_POST
def remove_from_wishlist(request, listing_id):
    """AJAX view for removing property from wishlist"""
    listing = get_object_or_404(Listing, id=listing_id)
    
    try:
        wishlist_item = Wishlist.objects.get(user=request.user, listing=listing)
        wishlist_item.delete()
        return JsonResponse({
            'success': True,
            'message': 'Property removed from your wishlist!',
            'action': 'removed'
        })
    except Wishlist.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Property is not in your wishlist.',
            'action': 'not_found'
        })


@login_required
def check_wishlist_status(request, listing_id):
    """AJAX view for checking if property is in user's wishlist"""
    is_in_wishlist = Wishlist.objects.filter(
        user=request.user, 
        listing_id=listing_id
    ).exists()
    
    return JsonResponse({
        'in_wishlist': is_in_wishlist
    })


# Super Admin functionality
def is_superuser(user):
    """Check if user is a superuser"""
    return user.is_superuser


@login_required
@user_passes_test(is_superuser)
def admin_all_listings(request):
    """View all listings for super-admin"""
    listings_list = Listing.objects.all().order_by('-list_date')
    
    # Search functionality
    if 'search' in request.GET:
        search = request.GET['search']
        if search:
            listings_list = listings_list.filter(title__icontains=search)
    
    # Status filter
    if 'status' in request.GET:
        status = request.GET['status']
        if status == 'published':
            listings_list = listings_list.filter(is_published=True)
        elif status == 'unpublished':
            listings_list = listings_list.filter(is_published=False)
    
    # Pagination
    paginator = Paginator(listings_list, 10)  # Show 10 listings per page
    page = request.GET.get('page')
    listings = paginator.get_page(page)
    
    context = {
        'listings': listings,
        'total_listings': Listing.objects.count(),
        'published_count': Listing.objects.filter(is_published=True).count(),
        'unpublished_count': Listing.objects.filter(is_published=False).count(),
        'values': request.GET
    }
    return render(request, 'accounts/admin_all_listings.html', context)


@login_required
@user_passes_test(is_superuser)
def admin_edit_listing(request, listing_id):
    """Edit any listing for super-admin"""
    from listings.models import Amenity
    listing = get_object_or_404(Listing, id=listing_id)
    
    if request.method == 'POST':
        # Get form data
        title = request.POST.get('title')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        description = request.POST.get('description')
        
        # Pricing fields
        price = request.POST.get('price')
        rent_price = request.POST.get('rent_price')
        deposit_amount = request.POST.get('deposit_amount')
        listing_type = request.POST.get('listing_type')
        
        # Property specifications
        property_type = request.POST.get('property_type')
        bedrooms = request.POST.get('bedrooms')
        bathrooms = request.POST.get('bathrooms')
        garage = request.POST.get('garage')
        sqft = request.POST.get('sqft')
        lot_size = request.POST.get('lot_size')
        year_built = request.POST.get('year_built')
        hoa_fee = request.POST.get('hoa_fee')
        energy_rating = request.POST.get('energy_rating')
        virtual_tour_url = request.POST.get('virtual_tour_url')
        
        # Admin controls
        is_published = request.POST.get('is_published') == 'on'
        featured = request.POST.get('featured') == 'on'
        
        # Amenities (many-to-many)
        amenities = request.POST.getlist('amenities')
        
        # Handle file uploads - only update if new files are provided
        photo_main = request.FILES.get('photo_main')
        photo_1 = request.FILES.get('photo_1')
        photo_2 = request.FILES.get('photo_2')
        photo_3 = request.FILES.get('photo_3')
        photo_4 = request.FILES.get('photo_4')
        photo_5 = request.FILES.get('photo_5')
        photo_6 = request.FILES.get('photo_6')
        
        # Update listing
        try:
            listing.title = title
            listing.address = address
            listing.city = city
            listing.state = state
            listing.zipcode = zipcode
            listing.description = description
            
            # Update pricing
            listing.price = int(price) if price else 0
            listing.rent_price = int(rent_price) if rent_price else None
            listing.deposit_amount = int(deposit_amount) if deposit_amount else None
            listing.listing_type = listing_type or 'sale'
            
            # Update property specifications
            listing.property_type = property_type or 'house'
            listing.bedrooms = int(bedrooms) if bedrooms else 0
            listing.bathrooms = float(bathrooms) if bathrooms else 0
            listing.garage = int(garage) if garage else 0
            listing.sqft = int(sqft) if sqft else 0
            listing.lot_size = float(lot_size) if lot_size else 0
            listing.year_built = int(year_built) if year_built else None
            listing.hoa_fee = float(hoa_fee) if hoa_fee else None
            listing.energy_rating = energy_rating or ''
            listing.virtual_tour_url = virtual_tour_url or ''
            
            # Update admin controls
            listing.is_published = is_published
            listing.featured = featured
            
            # Update photos only if new ones are provided
            if photo_main:
                listing.photo_main = photo_main
            if photo_1:
                listing.photo_1 = photo_1
            if photo_2:
                listing.photo_2 = photo_2
            if photo_3:
                listing.photo_3 = photo_3
            if photo_4:
                listing.photo_4 = photo_4
            if photo_5:
                listing.photo_5 = photo_5
            if photo_6:
                listing.photo_6 = photo_6
            
            listing.save()
            
            # Update amenities (many-to-many relationship)
            if amenities:
                listing.amenities.set(amenities)
            else:
                listing.amenities.clear()
            
            messages.success(request, f'Listing "{listing.title}" has been updated successfully!')
            return redirect('accounts:admin_all_listings')
            
        except Exception as e:
            messages.error(request, f'There was an error updating the listing: {str(e)}')
    
    # Get all amenities for the form
    all_amenities = Amenity.objects.all().order_by('name')
    
    context = {
        'listing': listing,
        'all_amenities': all_amenities,
    }
    return render(request, 'accounts/admin_edit_listing.html', context)


@login_required
@user_passes_test(is_superuser)
def admin_toggle_listing_status(request, listing_id):
    """Toggle listing published status"""
    listing = get_object_or_404(Listing, id=listing_id)
    listing.is_published = not listing.is_published
    listing.save()
    
    status = "published" if listing.is_published else "unpublished"
    messages.success(request, f'Listing "{listing.title}" has been {status}.')
    
    return redirect('accounts:admin_all_listings')
