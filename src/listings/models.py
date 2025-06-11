from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from realtors.models import Realtor


PROPERTY_TYPE_CHOICES = [
    ('house', 'House'),
    ('apartment', 'Apartment'),
    ('condo', 'Condo'),
    ('townhouse', 'Townhouse'),
    ('villa', 'Villa'),
    ('commercial', 'Commercial'),
    ('land', 'Land'),
    ('other', 'Other'),
]

LISTING_TYPE_CHOICES = [
    ('sale', 'For Sale'),
    ('rent', 'For Rent'),
    ('both', 'Sale or Rent'),
]


class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Amenities"
    
    def __str__(self):
        return self.name


class Listing(models.Model):
    realtor = models.ForeignKey(Realtor, on_delete=models.DO_NOTHING)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    
    # Listing type and pricing
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPE_CHOICES, default='sale')
    price = models.IntegerField(help_text="Price for sale")
    rent_price = models.IntegerField(null=True, blank=True, help_text="Monthly rent price")
    deposit_amount = models.IntegerField(null=True, blank=True, help_text="Security deposit for rent")
    
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
    garage = models.IntegerField(default=0)
    sqft = models.IntegerField()
    lot_size = models.DecimalField(max_digits=5, decimal_places=1)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(default=datetime.now, blank=True)
    
    # New enhanced fields
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES, default='house')
    year_built = models.IntegerField(null=True, blank=True)
    hoa_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Monthly HOA fee")
    view_count = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    amenities = models.ManyToManyField(Amenity, blank=True)
    virtual_tour_url = models.URLField(blank=True, help_text="Link to virtual tour")
    energy_rating = models.CharField(max_length=2, blank=True, help_text="A+ to F energy rating")
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def increment_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    def get_average_rating(self):
        reviews = self.propertyreview_set.all()
        if reviews:
            return sum([review.rating for review in reviews]) / len(reviews)
        return 0
    
    def get_review_count(self):
        return self.propertyreview_set.count()
    
    def get_display_price(self):
        """Get the appropriate price to display based on listing type"""
        if self.listing_type == 'rent':
            return f"${self.rent_price:,}/month" if self.rent_price else "Contact for Price"
        elif self.listing_type == 'both':
            sale_price = f"${self.price:,} (Sale)" if self.price else ""
            rent_price = f"${self.rent_price:,}/month (Rent)" if self.rent_price else ""
            if sale_price and rent_price:
                return f"{sale_price} or {rent_price}"
            return sale_price or rent_price or "Contact for Price"
        else:  # sale
            return f"${self.price:,}" if self.price else "Contact for Price"
    
    def is_for_sale(self):
        """Check if property is available for sale"""
        return self.listing_type in ['sale', 'both']
    
    def is_for_rent(self):
        """Check if property is available for rent"""
        return self.listing_type in ['rent', 'both']


class PropertyReview(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    title = models.CharField(max_length=200)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False, help_text="Verified review from actual visitor")
    
    class Meta:
        unique_together = ('listing', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.listing.title} - {self.user.username} ({self.rating}/5)"
