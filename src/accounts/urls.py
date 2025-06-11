from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    
    # Profile management
    path('profile/update/', views.profile_update, name='profile_update'),
    
    # Wishlist functionality
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:listing_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:listing_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/check/<int:listing_id>/', views.check_wishlist_status, name='check_wishlist_status'),
    
    # Super Admin URLs
    path('admin/listings/', views.admin_all_listings, name='admin_all_listings'),
    path('admin/listings/<int:listing_id>/edit/', views.admin_edit_listing, name='admin_edit_listing'),
    path('admin/listings/<int:listing_id>/toggle/', views.admin_toggle_listing_status, name='admin_toggle_listing_status'),
    
    # Super Admin Project URLs
    path('admin/projects/', views.admin_all_projects, name='admin_all_projects'),
    path('admin/projects/create/', views.admin_create_project, name='admin_create_project'),
    path('admin/projects/<int:project_id>/edit/', views.admin_edit_project, name='admin_edit_project'),
    path('admin/projects/<int:project_id>/delete/', views.admin_delete_project, name='admin_delete_project'),
    path('admin/projects/<int:project_id>/toggle/', views.admin_toggle_project_status, name='admin_toggle_project_status'),
    path('admin/projects/<int:project_id>/featured/', views.admin_toggle_project_featured, name='admin_toggle_project_featured'),
]
