# Vendor-Management-System-with-Performance-Metrics
This Django-based Vendor Management System allows you to manage vendors, track purchase orders, and calculate performance metrics such as on-time delivery rate, quality rating average, response time, and fulfillment rate.

# Setup Instructions
# Clone the Repository
git clone `https://github.com/python-hacked/Vendor-Management-System-with-Performance-Metrics.git`

# Install Dependencies
pip install -r requirements.txt

# Database Migration
python manage.py migrate

# Start the Development Server
python manage.py runserver

# Accessing the APIOpen your browser or a tool like Postman and navigate to http://localhost:8000/ to access the API endpoints.


# Create a New Vendor
Endpoint: POST /api/vendors/
# Input:
{
  "name": "Vendor Name",
  "contact_details": "Contact Information",
  "address": "Vendor Address",
  "vendor_code": "Unique Vendor Code"
}

# Output:
{
  "id": 1,
  "name": "Vendor Name",
  "contact_details": "Contact Information",
  "address": "Vendor Address",
  "vendor_code": "Unique Vendor Code",
  "on_time_delivery_rate": 0.0,
  "quality_rating_avg": 0.0,
  "average_response_time": 0.0,
  "fulfillment_rate": 0.0
}

# List All Vendors
# Endpoint: GET /api/vendors/
# Output:
[
  {
    "id": 1,
    "name": "Vendor Name",
    "contact_details": "Contact Information",
    "address": "Vendor Address",
    "vendor_code": "Unique Vendor Code",
    "on_time_delivery_rate": 0.0,
    "quality_rating_avg": 0.0,
    "average_response_time": 0.0,
    "fulfillment_rate": 0.0
  },
  ...
]

# Retrieve a Specific Vendor
# Endpoint: GET /api/vendors/{vendor_id}/
# Output

{
  "id": 1,
  "name": "Vendor Name",
  "contact_details": "Contact Information",
  "address": "Vendor Address",
  "vendor_code": "Unique Vendor Code",
  "on_time_delivery_rate": 0.0,
  "quality_rating_avg": 0.0,
  "average_response_time": 0.0,
  "fulfillment_rate": 0.0
}

# Update a Vendor
# Endpoint: PUT /api/vendors/{vendor_id}/
# Input:
{
  "name": "Updated Vendor Name",
  "contact_details": "Updated Contact Information",
  "address": "Updated Vendor Address",
  "vendor_code": "Updated Unique Vendor Code"
}

# Output:
{
  "message": "Vendor updated successfully"
}

# Delete a Vendor
# Endpoint: DELETE /api/vendors/{vendor_id}/
# Output:
{
  "message": "Vendor deleted successfully"
}

## Purchase Order Management ##
# Endpoint: POST /api/purchase_orders/
# Input
{
  "po_number": "PO123",
  "vendor": 1,
  "order_date": "2024-05-05T12:00:00Z",
  "delivery_date": "2024-05-10T12:00:00Z",
  "items": {"item1": "description1", "item2": "description2"},
  "quantity": 100,
  "status": "pending"
}

# Output:
{
  "po_number": "PO123",
  "vendor": 1,
  "order_date": "2024-05-05T12:00:00Z",
  "delivery_date": "2024-05-10T12:00:00Z",
  "items": {"item1": "description1", "item2": "description2"},
  "quantity": 100,
  "status": "pending"
}

# List All Purchase Orders
# Endpoint: GET /api/purchase_orders/
# Output
[
  {
    "po_number": "PO123",
    "vendor": 1,
    "order_date": "2024-05-05T12:00:00Z",
    "delivery_date": "2024-05-10T12:00:00Z",
    "items": {"item1": "description1", "item2": "description2"},
    "quantity": 100,
    "status": "pending"
  },
  ...
]

# Retrieve a Specific Purchase Order
# Endpoint: GET /api/purchase_orders/{po_number}/
# Output:
{
  "po_number": "PO123",
  "vendor": 1,
  "order_date": "2024-05-05T12:00:00Z",
  "delivery_date": "2024-05-10T12:00:00Z",
  "items": {"item1": "description1", "item2": "description2"},
  "quantity": 100,
  "status": "pending"
}

# Update a Purchase Order
# Endpoint: PUT /api/purchase_orders/{po_number}/
# Input
{
  "status": "completed",
  "quality_rating": 4.5,
  "acknowledgment_date": "2024-05-06T12:00:00Z"
}

# Output
{
  "po_number": "PO123",
  "vendor": 1,
  "order_date": "2024-05-05T12:00:00Z",
  "delivery_date": "2024-05-10T12:00:00Z",
  "items": {"item1": "description1", "item2": "description2"},
  "quantity": 100,
  "status": "completed",
  "quality_rating": 4.5,
  "acknowledgment_date": "2024-05-06T12:00:00Z"
}

# Delete a Purchase Order
# Endpoint: DELETE /api/purchase_orders/{po_number}/
# Output:
{
  "message": "Purchase Order with po_number 'PO123' deleted successfully"
}

## Vendor Performance Metrics ##

# Retrieve Vendor Performance Metrics
# Endpoint: GET /api/vendors/{vendor_id}/performance/
# Output
{
  "vendor_id": 1,
  "name": "Vendor Name",
  "on_time_delivery_rate": 80.0,
  "quality_rating_avg": 4.2,
  "average_response_time": 86400.0,
  "fulfillment_rate": 95.0
}

# Additional Notes
@ create admin and use Token 
# python manage.py createsuperuser

$ Token-based authentication is required to access the API endpoints. Obtain a token from the administrator for authentication.
For testing purposes, use tools like Postman or cURL to send requests to the API endpoints and validate the responses.
Ensure data integrity by handling edge cases such as missing data points or invalid inputs gracefully within the views and serializers.

