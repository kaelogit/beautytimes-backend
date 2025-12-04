from django.db import models

class Category(models.Model):
    """Defines product categories (e.g., Face Creams, Body Care)."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories" # Fixes display name in Admin

    def __str__(self):
        return self.name

class Product(models.Model):
    """Defines the product structure for the e-commerce inventory."""
    
    # Core Product Info
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True, blank=True)
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Details
    description = models.TextField()
    
    # Status and Promotion Flags (used for homepage filtering and admin filtering)
    is_new = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=True)
    
    # Inventory Tracking
    stock_quantity = models.IntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
        
    def get_discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            return round(((self.original_price - self.price) / self.original_price) * 100)
        return 0

class ProductImage(models.Model):
    """Stores multiple images linked to a single product."""
    product = models.ForeignKey(
        Product, 
        related_name='images', 
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='products/') 
    is_main = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Product Image"
        
    def __str__(self):
        return f"Image for {self.product.title}"

class Subscriber(models.Model):
    email = models.EmailField(unique=True) # Unique ensures no duplicate emails
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.name}"
    
# ... existing code ...

class Order(models.Model):
    # Customer Info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Shipping Info
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    
    # Order Details
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending') # Pending, Paid, Shipped
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.first_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Price at time of purchase
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product.title if self.product else 'Unknown'}"