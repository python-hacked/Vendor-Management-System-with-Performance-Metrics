from django.urls import path
from . import views

urlpatterns = [
    path('api/vendors/', views.create_vendor, name='create-vendor'),
    path('api/vendors/<int:vendor_id>/', views.retrieve_vendor, name='retrieve-vendor'),
    path('api/vendors/<int:vendor_id>/update/', views.update_vendor, name='update-vendor'),
    path('api/vendors/<int:vendor_id>/delete/', views.delete_vendor, name='delete-vendor'),
    path('api/vendors/all/', views.list_vendors, name='list-vendors'),
]
