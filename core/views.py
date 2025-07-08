from django.shortcuts import render, redirect
from django.views import View
def alfissen_detail_view(request):
    return render(request, 'core/alfissen_detail.html')

def ouakkaha_detail_view(request):
    return render(request, 'core/ouakkaha_detail.html')
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from products.models import Product
from orders.models import Order
from users.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from decimal import Decimal

def home_view(request):
    # Get products from the database
    all_products = Product.objects.all()[:8]
    poussins = Product.objects.filter(type=Product.POUSSINS)[:4]
    aliments = Product.objects.filter(type=Product.ALIMENTS)[:4]
    
    # Create context with database products
    context = {
        'products': all_products,
        'poussins': poussins,
        'aliments': aliments,
    }
    
    return render(request, 'core/home.html', context)




class AdminDashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'core/admin_dashboard.html'
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == User.ADMIN
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Product statistics
        context['total_products'] = Product.objects.count()
        context['poussins_count'] = Product.objects.filter(type=Product.POUSSINS).count()
        context['aliments_count'] = Product.objects.filter(type=Product.ALIMENTS).count()
        
        # User statistics
        context['total_users'] = User.objects.count()
        context['alfissen_count'] = User.objects.filter(role=User.ALFISSEN).count()
        context['ouakkaha_count'] = User.objects.filter(role=User.OUAKKAHA).count()
        context['customer_count'] = User.objects.filter(role=User.CUSTOMER).count()
        
        # Order statistics
        context['total_orders'] = Order.objects.count()
        context['pending_orders'] = Order.objects.filter(status=Order.PENDING).count()
        context['total_sales'] = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
        
        # Recent data
        context['recent_orders'] = Order.objects.all()[:10]
        context['recent_users'] = User.objects.all().order_by('-date_joined')[:10]
        context['recent_products'] = Product.objects.all()[:10]
        
        return context

class AlfissenDashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'core/alfissen_dashboard.html'
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == User.ALFISSEN
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Product statistics
        context['my_products'] = Product.objects.filter(seller=user)
        context['product_count'] = context['my_products'].count()
        
        # Sales statistics (orders containing this user's products)
        from orders.models import OrderItem
        
        # Get all order items for this seller's products
        sale_items = OrderItem.objects.filter(product__seller=user)
        context['sales'] = sale_items
        context['sales_count'] = sale_items.count()
        
        # Safely calculate total sales
        if sale_items:
            context['sales_total'] = sum(item.get_cost() for item in sale_items)
        else:
            context['sales_total'] = 0
        
        # Get unique orders containing this seller's products
        order_ids = sale_items.values_list('order', flat=True).distinct()
        context['sales_orders'] = Order.objects.filter(id__in=order_ids).order_by('-created_at')
        context['sales_orders_count'] = context['sales_orders'].count()
        
        # Count orders by status
        context['pending_orders'] = context['sales_orders'].filter(status=Order.PENDING).count()
        context['processing_orders'] = context['sales_orders'].filter(status=Order.PROCESSING).count()
        context['shipped_orders'] = context['sales_orders'].filter(status=Order.SHIPPED).count()
        context['delivered_orders'] = context['sales_orders'].filter(status=Order.DELIVERED).count()
        context['cancelled_orders'] = context['sales_orders'].filter(status=Order.CANCELLED).count()
        
        return context

class OuakkahaDashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'core/ouakkaha_dashboard.html'
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == User.OUAKKAHA
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Product statistics
        context['my_products'] = Product.objects.filter(seller=user)
        context['product_count'] = context['my_products'].count()
        
        # Sales statistics (orders containing this user's products)
        from orders.models import OrderItem
        
        # Get all order items for this seller's products
        sale_items = OrderItem.objects.filter(product__seller=user)
        context['sales'] = sale_items
        context['sales_count'] = sale_items.count()
        
        # Safely calculate total sales
        if sale_items:
            context['sales_total'] = sum(item.get_cost() for item in sale_items)
        else:
            context['sales_total'] = 0
        
        # Get unique orders containing this seller's products
        order_ids = sale_items.values_list('order', flat=True).distinct()
        context['sales_orders'] = Order.objects.filter(id__in=order_ids).order_by('-created_at')
        context['sales_orders_count'] = context['sales_orders'].count()
        
        # Count orders by status
        context['pending_orders'] = context['sales_orders'].filter(status=Order.PENDING).count()
        context['processing_orders'] = context['sales_orders'].filter(status=Order.PROCESSING).count()
        context['shipped_orders'] = context['sales_orders'].filter(status=Order.SHIPPED).count()
        context['delivered_orders'] = context['sales_orders'].filter(status=Order.DELIVERED).count()
        context['cancelled_orders'] = context['sales_orders'].filter(status=Order.CANCELLED).count()
        
        return context
