from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. Admin Site
    path('admin/', admin.site.urls),
    
    # 2. General Project Root (Will include all inventory URLs)
    path('', include('inventory.urls')), 
]

