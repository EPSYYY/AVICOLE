from django.db import models
from django.conf import settings
from django.urls import reverse

class Product(models.Model):
    POUSSINS = 'poussins'
    ALIMENTS = 'aliments'
    
    PRODUCT_TYPES = [
        (POUSSINS, 'Poussins'),
        (ALIMENTS, 'Aliments Composés'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=10, choices=PRODUCT_TYPES)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    details_image = models.ImageField(upload_to='products/details/', null=True, blank=True, help_text="Image showing product details")
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.id])
    
    @property
    def is_in_stock(self):
        return self.stock > 0
