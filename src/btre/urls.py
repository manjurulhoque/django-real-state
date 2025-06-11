from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('pages.urls')),
    path('', include('accounts.urls')),
    path('', include('contacts.urls')),
    path('listings/', include('listings.urls')),
    path('projects/', include('projects.urls')),
    #api
    path('api/', include('listings.api.urls')),
    path('api/', include('accounts.api.urls')),
    path('api/', include('pages.api.urls')),
    path('super-admin/', admin.site.urls),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
