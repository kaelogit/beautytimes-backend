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

# CRITICAL FIX: Ensure static() returns a list and adds to the list
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)