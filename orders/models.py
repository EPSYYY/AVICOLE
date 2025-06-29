from django.db import models
from django.conf import settings
from products.models import Product

class Order(models.Model):
    PENDING = 'pending'
    PROCESSING = 'processing'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    shipping_address = models.TextField()
    phone_number = models.CharField(max_length=15)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
    
    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def save(self, *args, **kwargs):
        # Only calculate total_price if not explicitly set and items exist
        if not self.pk or (not self.total_price and hasattr(self, 'items')):
            try:
                self.total_price = self.get_total_price()
            except:
                pass  # If items don't exist yet, we'll set the price later
        super().save(*args, **kwargs)
    
    def cancel_order(self):
        """Cancel the order and restore product stock"""
        if self.status != self.CANCELLED:
            # Restore product stock
            for item in self.items.all():
                product = item.product
                product.stock += item.quantity
                product.save()
            
            self.status = self.CANCELLED
            self.save()
            return True
        return False
    
    def accept_order(self):
        """Accept the order and change status to processing"""
        if self.status == self.PENDING:
            self.status = self.PROCESSING
            self.save()
            return True
        return False
        
    def can_be_cancelled(self):
        """Check if order can be cancelled (only pending orders)"""
        return self.status == self.PENDING

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def get_cost(self):
        return self.price * self.quantity

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart of {self.user.username}"
    
    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def clear(self):
        self.items.all().delete()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ('cart', 'product')
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def get_cost(self):
        return self.product.price * self.quantity
