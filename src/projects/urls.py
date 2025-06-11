from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='projects'),
    path('<int:project_id>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('search/', views.search_projects, name='search'),
    path('<int:project_id>/inquiry/', views.project_inquiry, name='project_inquiry'),
    path('my-inquiries/', views.my_project_inquiries, name='my_inquiries'),
] 