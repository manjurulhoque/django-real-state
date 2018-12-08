from django.contrib import admin

# Register your models here.
from listings.models import Listing

admin.site.register(Listing)