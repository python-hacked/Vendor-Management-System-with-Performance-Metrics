from django.shortcuts import render
from . models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PurchaseOrderSerializer,VendorSerializer


# Create your views here.
# @csrf_exempt
def create_vendor(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            new_vendor = Vendor.objects.create(
                name=data['name'],
                contact_details=data['contact_details'],
                address=data['address'],
                vendor_code=data['vendor_code']
            )
            return JsonResponse({'message': 'Vendor created successfully', 'id': new_vendor.id}, status=201)
        except IntegrityError:
            return JsonResponse({'error': 'Vendor code must be unique'}, status=400)
        except KeyError:
            return JsonResponse({'error': 'Invalid data provided'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def list_vendors(request):
    if request.method == 'GET':
        vendors = Vendor.objects.all()
        vendor_list = list(vendors.values())
        return JsonResponse(vendor_list, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def retrieve_vendor(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return JsonResponse({'error': 'Vendor not found'}, status=404)

    if request.method == 'GET':
        vendor_data = {
            'id': vendor.id,
            'name': vendor.name,
            'contact_details': vendor.contact_details,
            'address': vendor.address,
            'vendor_code': vendor.vendor_code,
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate
        }
        return JsonResponse(vendor_data)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def update_vendor(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return JsonResponse({'error': 'Vendor not found'}, status=404)

    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            vendor.name = data['name']
            vendor.contact_details = data['contact_details']
            vendor.address = data['address']
            vendor.vendor_code = data['vendor_code']
            vendor.save()
            return JsonResponse({'message': 'Vendor updated successfully'})
        except KeyError:
            return JsonResponse({'error': 'Invalid data provided'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

# @csrf_exempt
def delete_vendor(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return JsonResponse({'error': 'Vendor not found'}, status=404)

    if request.method == 'DELETE':
        vendor.delete()
        return JsonResponse({'message': 'Vendor deleted successfully'}, status=204)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@api_view(['POST'])
def create_purchase_order(request):
    serializer = PurchaseOrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_purchase_order(request, po_number):
    try:
        purchase_order = PurchaseOrder.objects.get(po_number=po_number)
    except PurchaseOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PurchaseOrderSerializer(purchase_order)
    return Response(serializer.data)



@api_view(['GET'])
def list_purchase_orders(request):
    try:
        purchase_orders = PurchaseOrder.objects.all()  # QuerySet of all PurchaseOrder instances
    except PurchaseOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PurchaseOrderSerializer(purchase_orders, many=True)  # Serialize queryset (many=True for multiple instances)
    return Response(serializer.data)

@api_view(['PUT'])
def update_purchase_order(request, po_number):
    try:
        purchase_order = PurchaseOrder.objects.get(po_number=po_number)
    except PurchaseOrder.DoesNotExist:
        return Response({"message": f"Purchase Order with po_number '{po_number}' not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_purchase_order(request, po_number):
    try:
        purchase_order = PurchaseOrder.objects.get(po_number=po_number)
    except PurchaseOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    purchase_order.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_vendor_performance(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Calculate performance metrics based on related HistoricalPerformance records
    historical_performance = HistoricalPerformance.objects.filter(vendor=vendor)

    if not historical_performance.exists():
        return Response({"message": "No historical performance data available for this vendor."}, 
                        status=status.HTTP_404_NOT_FOUND)

    total_orders = historical_performance.count()
    on_time_delivery_count = historical_performance.filter(on_time_delivery_rate__gte=0.8).count()
    quality_ratings = historical_performance.values_list('quality_rating_avg', flat=True)
    average_quality_rating = sum(quality_ratings) / total_orders if total_orders > 0 else 0.0
    response_times = historical_performance.values_list('average_response_time', flat=True)
    average_response_time = sum(response_times) / total_orders if total_orders > 0 else 0.0
    fulfilled_orders_count = historical_performance.filter(fulfillment_rate__gte=0.9).count()

    # Update vendor's performance metrics
    vendor.on_time_delivery_rate = (on_time_delivery_count / total_orders) * 100
    vendor.quality_rating_avg = average_quality_rating
    vendor.average_response_time = average_response_time
    vendor.fulfillment_rate = (fulfilled_orders_count / total_orders) * 100
    vendor.save()

    # Prepare response data
    response_data = {
        "vendor_id": vendor.id,
        "name": vendor.name,
        "on_time_delivery_rate": vendor.on_time_delivery_rate,
        "quality_rating_avg": vendor.quality_rating_avg,
        "average_response_time": vendor.average_response_time,
        "fulfillment_rate": vendor.fulfillment_rate
    }

    return Response(response_data, status=status.HTTP_200_OK)




@api_view(['GET'])
def get_vendor_performance(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response({"message": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

    # Update performance metrics before retrieving
    vendor.update_performance_metrics()

    serializer = VendorSerializer(vendor)
    return Response(serializer.data, status=status.HTTP_200_OK)