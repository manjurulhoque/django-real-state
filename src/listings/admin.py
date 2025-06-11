from django.contrib import admin
from .models import Listing, Amenity, PropertyReview


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'city', 'state', 'price', 'property_type', 'is_published', 'featured', 'view_count', 'list_date')
    list_display_links = ('id', 'title')
    list_filter = ('is_published', 'featured', 'property_type', 'city', 'state', 'realtor')
    list_editable = ('is_published', 'featured')
    search_fields = ('title', 'address', 'city', 'state', 'zipcode', 'description')
    list_per_page = 25
    filter_horizontal = ('amenities',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'address', 'city', 'state', 'zipcode', 'description', 'realtor', 'submitted_by')
        }),
        ('Property Details', {
            'fields': ('property_type', 'price', 'bedrooms', 'bathrooms', 'garage', 'sqft', 'lot_size', 'year_built', 'hoa_fee', 'energy_rating')
        }),
        ('Features', {
            'fields': ('amenities', 'virtual_tour_url')
        }),
        ('Media', {
            'fields': ('photo_main', 'photo_1', 'photo_2', 'photo_3', 'photo_4', 'photo_5', 'photo_6')
        }),
        ('Status', {
            'fields': ('is_published', 'featured', 'view_count')
        }),
        ('Timestamps', {
            'fields': ('list_date', 'last_updated'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('view_count', 'last_updated')


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'created_at')
    search_fields = ('name',)
    list_per_page = 25


@admin.register(PropertyReview)
class PropertyReviewAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'rating', 'title', 'is_verified', 'created_at')
    list_filter = ('rating', 'is_verified', 'created_at')
    search_fields = ('listing__title', 'user__username', 'title', 'review')
    list_per_page = 25
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_verified',)