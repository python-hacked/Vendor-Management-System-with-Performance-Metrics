from django.shortcuts import render
from . models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import IntegrityError


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


