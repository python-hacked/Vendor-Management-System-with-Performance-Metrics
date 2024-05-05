from django.urls import path
from . import views

urlpatterns = [
    path('api/vendors/', views.create_vendor, name='create-vendor'),
    path('api/vendors/<int:vendor_id>/', views.retrieve_vendor, name='retrieve-vendor'),
    path('api/vendors/<int:vendor_id>/update/', views.update_vendor, name='update-vendor'),
    path('api/vendors/<int:vendor_id>/delete/', views.delete_vendor, name='delete-vendor'),
    path('api/vendors/all/', views.list_vendors, name='list-vendors'),
    path('api/purchase_orders/', views.list_purchase_orders, name='purchase-order-list'),
    path('api/purchase_orders/create/', views.create_purchase_order, name='purchase-order-create'),
    path('api/purchase_orders/<str:po_number>/', views.get_purchase_order, name='purchase-order-detail'),
    path('api/purchase_orders/<str:po_number>/update/',views.update_purchase_order, name='purchase-order-update'),
    path('api/purchase_orders/<str:po_number>/delete/',views.delete_purchase_order, name='purchase-order-delete'),
    path('api/vendors/<int:vendor_id>/performance/', views.get_vendor_performance, name='vendor-performance'),

]

