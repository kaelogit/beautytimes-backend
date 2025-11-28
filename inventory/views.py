import json  # <--- CRITICAL: Needed for reading data
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

# CRITICAL FIX: Ensure Order and OrderItem are included in this list
from .models import Product, Category, ProductImage, Subscriber, ContactMessage, Order, OrderItem

# --- 1. THE MISSING FUNCTION ---
def home_page(request):
    return HttpResponse("<h1>Welcome to the Django Backend! <br> Go to <a href='/admin/'>/admin/</a> to manage products.</h1>")

# --- 2. THE API FUNCTION ---
def get_products_api(request):
    """Retrieves all products and their associated images from the database and returns them as JSON."""
    
    # Get all products, pre-fetching categories and images for efficiency
    products_qs = Product.objects.all().select_related('category').prefetch_related('images')
    
    products_list = []
    for product in products_qs:
        product_dict = model_to_dict(product)
        
        # Add category slug/name for frontend filtering
        if product.category:
            product_dict['category'] = product.category.slug
        else:
            product_dict['category'] = 'uncategorized'
            
        # GATHER ALL IMAGE URLs FOR THE GALLERY
        image_records = ProductImage.objects.filter(product=product)
        
        product_dict['image_gallery'] = [
            {'url': img.image_url, 'is_main': img.is_main} 
            for img in image_records
        ]
        
        # Determine the main image URL for the main card display
        main_image = next((img for img in product_dict['image_gallery'] if img['is_main']), None)
        
        # If no main image is found, default to the first image in the gallery
        if not main_image and product_dict['image_gallery']:
            main_image = product_dict['image_gallery'][0]

        product_dict['image'] = main_image['url'] if main_image else ''
        
        # Add the discount calculation
        product_dict['discount_percentage'] = product.get_discount_percentage()
        
        products_list.append(product_dict)

    # Return the data as a JSON response
    return JsonResponse(products_list, safe=False)

@csrf_exempt # Allows the frontend to send data without a security token (for now)
def newsletter_signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            
            # Check if email is valid
            if not email:
                return JsonResponse({'success': False, 'message': 'Email is required.'}, status=400)

            # Try to create the subscriber
            subscriber, created = Subscriber.objects.get_or_create(email=email)
            
            if created:
                return JsonResponse({'success': True, 'message': 'Thank you for subscribing!'})
            else:
                return JsonResponse({'success': False, 'message': 'You are already subscribed!'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
            
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)


@csrf_exempt
def contact_submission(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Create the message in the database
            ContactMessage.objects.create(
                name=data.get('name'),
                email=data.get('email'),
                subject=data.get('subject'),
                message=data.get('message')
            )
            return JsonResponse({'success': True, 'message': 'Message sent successfully!'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Error sending message.'}, status=500)
            
    return JsonResponse({'success': False, 'message': 'Invalid request.'}, status=400)

@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            customer_data = data.get('customer')
            items_data = data.get('items')
            total_amount = data.get('total_amount')

            # 1. Create the Main Order
            order = Order.objects.create(
                first_name=customer_data.get('first_name'),
                last_name=customer_data.get('last_name'),
                email=customer_data.get('email'),
                phone=customer_data.get('phone'),
                address=customer_data.get('address'),
                city=customer_data.get('city'),
                state=customer_data.get('state'),
                total_amount=total_amount
            )

            # 2. Create Order Items
            for item in items_data:
                product = Product.objects.get(id=item['product_id'])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=item['price'],
                    quantity=item['quantity']
                )

            return JsonResponse({'success': True, 'order_id': order.id, 'message': 'Order created successfully'})

        except Exception as e:
            print(f"Error creating order: {e}")
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)


@csrf_exempt
def update_payment_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_id = data.get('order_id')
            payment_reference = data.get('reference')

            # 1. Find the Order
            order = Order.objects.get(id=order_id)
            
            # 2. Update Status
            order.status = 'Paid'
            # You might want to save the payment reference too if you add a field for it later
            order.save()

            return JsonResponse({'success': True, 'message': 'Payment status updated'})

        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Order not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)