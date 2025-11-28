from django.contrib import admin
from .models import Category, Product, ProductImage, Subscriber, ContactMessage, Order, OrderItem # <--- Added new imports

# Define the Inline editor for images
class ProductImageInline(admin.TabularInline): 
    model = ProductImage
    extra = 1

# Register Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)} 

# Register Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline] 
    list_display = ('title', 'brand', 'price', 'category', 'is_bestseller', 'in_stock')
    list_filter = ('category', 'brand', 'is_bestseller', 'in_stock')
    search_fields = ('title', 'brand', 'sku')
    date_hierarchy = 'created_at'
    fields = (
        ('title', 'brand'),
        'sku',
        ('price', 'original_price'),
        'category',
        'description',
        'stock_quantity',
        ('is_new', 'is_bestseller', 'in_stock')
    )

# --- NEW REGISTRATIONS BELOW ---

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'created_at') # Columns to show in the list
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at') # Make read-only so you don't accidentally edit them

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_subscribed')
    search_fields = ('email',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity') # Prevent changing history

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline] # Shows items inside the order page
    readonly_fields = ('created_at',)