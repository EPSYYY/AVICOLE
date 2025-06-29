from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'type', 'seller', 'created_at']
    list_filter = ['type', 'seller', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'description', 'price', 'stock', 'type', 'image')
        }),
        ('Seller Information', {
            'fields': ('seller',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
