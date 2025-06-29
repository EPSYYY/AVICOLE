from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product
from .forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from users.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    login_required = False
    
    def get_queryset(self):
        queryset = Product.objects.all()
        q = self.request.GET.get('q')
        product_type = self.request.GET.get('type')
        seller_id = self.request.GET.get('seller')
        
        # Restrict products for sellers
        user = self.request.user
        if user.is_authenticated:
            if user.role == User.ALFISSEN:
                # Alfissen can only see their own products
                queryset = queryset.filter(seller=user, type=Product.ALIMENTS)
            elif user.role == User.OUAKKAHA:
                # Ouakkaha can only see their own products
                queryset = queryset.filter(seller=user, type=Product.POUSSINS)
            elif user.role == User.ADMIN:
                # Admin can see all products and filter by type
                if product_type:
                    queryset = queryset.filter(type=product_type)
                if seller_id:
                    queryset = queryset.filter(seller_id=seller_id)
        else:
            # For customers and anonymous users
            if product_type:
                queryset = queryset.filter(type=product_type)
            if seller_id:
                queryset = queryset.filter(seller_id=seller_id)
        
        # Search functionality
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) | Q(description__icontains=q)
            )
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_types'] = Product.PRODUCT_TYPES
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    login_required = False

class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    template_name = 'products/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('products:product_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.seller = self.request.user
        messages.success(self.request, "Product created successfully!")
        return super().form_valid(form)
    
    def test_func(self):
        user = self.request.user
        # Only Alfissen and Ouakkaha users can create products
        return user.role == User.ALFISSEN or user.role == User.OUAKKAHA or user.role == User.ADMIN

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    template_name = 'products/product_form.html'
    form_class = ProductForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, "Product updated successfully!")
        return super().form_valid(form)
    
    def test_func(self):
        product = self.get_object()
        user = self.request.user
        
        # Check if user is the seller or admin
        return user == product.seller or user.role == User.ADMIN

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('products:product_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Product deleted successfully!")
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        product = self.get_object()
        user = self.request.user
        
        # Check if user is the seller or admin
        return user == product.seller or user.role == User.ADMIN

@csrf_exempt
def search_suggestions(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(name__istartswith=query)[:10]
        suggestions = [{'id': product.id, 'name': product.name, 'url': product.get_absolute_url()} for product in products]
        return JsonResponse(suggestions, safe=False)
    return JsonResponse([], safe=False)
