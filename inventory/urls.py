from django.urls import path
from . import views

urlpatterns = [
    # 1. The API endpoint MUST come before the home page.
    path('api/products/', views.get_products_api, name='products_api'),
    
    # 2. The general root path for the welcome message.
    path('', views.home_page, name='home'),

    path('api/newsletter/', views.newsletter_signup, name='newsletter_signup'),

    path('api/contact/', views.contact_submission, name='contact_submission'),

    path('api/create-order/', views.create_order, name='create_order'),

    path('api/update-payment/', views.update_payment_status, name='update_payment'),
]