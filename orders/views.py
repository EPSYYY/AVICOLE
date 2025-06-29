from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseForbidden
from .models import Order, OrderItem, Cart, CartItem
from .forms import CartAddProductForm, OrderCreateForm
from products.models import Product
from users.models import User

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        quantity = cd['quantity']
        update = cd['update']
        
        # Check if seller role restrictions apply
        user = request.user
        seller = product.seller
        
        # Role-based purchase restrictions
        if user.role == User.ALFISSEN and seller.role == User.ALFISSEN:
            messages.error(request, "Alfissen users cannot buy from other Alfissen users.")
            return redirect('products:product_detail', product_id)
        
        if user.role == User.OUAKKAHA and seller.role == User.OUAKKAHA:
            messages.error(request, "Ouakkaha users cannot buy from other Ouakkaha users.")
            return redirect('products:product_detail', product_id)
        
        # Check stock availability
        if quantity > product.stock:
            messages.error(request, f"Sorry, only {product.stock} items are available.")
            return redirect('products:product_detail', product_id)
        
        # Get or create cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Get or create cart item
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            if update:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity
                
            # Check if the updated quantity exceeds stock
            if cart_item.quantity > product.stock:
                messages.error(request, f"Sorry, only {product.stock} items are available.")
                return redirect('products:product_detail', product_id)
                
            cart_item.save()
        except CartItem.DoesNotExist:
            CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        
        messages.success(request, f"{product.name} added to your cart.")
    
    return redirect('orders:cart_detail')

@login_required
def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        messages.success(request, f"{product.name} removed from your cart.")
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        pass
    
    return redirect('orders:cart_detail')

@login_required
def cart_detail(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
    except Cart.DoesNotExist:
        cart = None
        cart_items = []
    
    total = sum(item.get_cost() for item in cart_items) if cart_items else 0
    
    return render(request, 'orders/cart_detail.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total': total
    })

@login_required
def order_create(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
    except Cart.DoesNotExist:
        messages.error(request, "Your cart is empty.")
        return redirect('products:product_list')
    
    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect('products:product_list')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            # Don't calculate total price yet
            order.save()
            
            # Create order items and update stock
            total_price = 0
            for item in cart_items:
                product = item.product
                
                # Check if product is still in stock
                if item.quantity > product.stock:
                    messages.error(request, f"Sorry, {product.name} only has {product.stock} items left.")
                    order.delete()
                    return redirect('orders:cart_detail')
                
                # Calculate item cost
                item_cost = product.price * item.quantity
                total_price += item_cost
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.price,
                    quantity=item.quantity
                )
                
                # Update stock
                product.stock -= item.quantity
                product.save()
            
            # Update order total price
            order.total_price = total_price
            order.save()
            
            # Clear the cart
            cart.clear()
            
            messages.success(request, "Your order has been placed successfully!")
            return redirect('orders:order_detail', order.id)
    else:
        form = OrderCreateForm()
    
    return render(request, 'orders/order_create.html', {
        'form': form,
        'cart_items': cart_items,
        'total': sum(item.get_cost() for item in cart_items)
    })

@login_required
def order_list(request):
    user = request.user
    
    # Filter orders based on user role
    if user.role == User.ADMIN:
        # Admin sees all orders
        orders = Order.objects.all()
    elif user.role in (User.ALFISSEN, User.OUAKKAHA):
        # Sellers see orders containing their products
        # First get all order items for products sold by this user
        seller_order_items = OrderItem.objects.filter(product__seller=user)
        order_ids = seller_order_items.values_list('order', flat=True).distinct()
        orders = Order.objects.filter(id__in=order_ids)
    else:
        # Customers see their own orders
        orders = Order.objects.filter(user=user)
        
    return render(request, 'orders/order_list.html', {
        'orders': orders,
        'is_seller': user.role in (User.ALFISSEN, User.OUAKKAHA)
    })

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Check if the user is allowed to view this order
    user = request.user
    
    # Admin can view all orders
    if user.role == User.ADMIN:
        pass  # Admin can view all orders
    # Order owner can view the order
    elif order.user == user:
        pass  # Customer can view their own order
    # Seller can view orders containing their products
    else:
        # Check if any items in the order are sold by this user
        seller_items = order.items.filter(product__seller=user)
        if not seller_items.exists():
            return HttpResponseForbidden("You don't have permission to view this order.")
    
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Check permissions
    if request.user.role == User.ADMIN:
        # Admin can cancel any order
        can_cancel = True
    elif order.user == request.user:
        # User can cancel their own orders if still pending
        can_cancel = order.can_be_cancelled()
    else:
        # Seller can cancel orders for their products if still pending
        seller_items = order.items.filter(product__seller=request.user)
        can_cancel = seller_items.exists() and order.can_be_cancelled()
    
    if can_cancel:
        order.cancel_order()
        messages.success(request, f"Order #{order.id} has been cancelled.")
    else:
        messages.error(request, "You don't have permission to cancel this order or the order cannot be cancelled.")
    
    # Redirect back to appropriate page
    if request.user.role in (User.ALFISSEN, User.OUAKKAHA):
        # Seller goes back to dashboard
        if request.user.role == User.ALFISSEN:
            return redirect('core:alfissen_dashboard')
        else:
            return redirect('core:ouakkaha_dashboard')
    else:
        # Customer or admin goes to order detail
        return redirect('orders:order_detail', order.id)

@login_required
def order_accept(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Check permissions - only sellers and admins can accept orders
    if request.user.role == User.ADMIN:
        # Admin can accept any order
        can_accept = True
    elif request.user.role in (User.ALFISSEN, User.OUAKKAHA):
        # Seller can accept orders for their products
        seller_items = order.items.filter(product__seller=request.user)
        can_accept = seller_items.exists()
    else:
        can_accept = False
    
    if can_accept and order.status == Order.PENDING:
        order.accept_order()
        messages.success(request, f"Order #{order.id} has been accepted and is now being processed.")
    else:
        messages.error(request, "You don't have permission to accept this order or the order cannot be accepted.")
    
    # Redirect back to appropriate page
    if request.user.role in (User.ALFISSEN, User.OUAKKAHA):
        # Seller goes back to dashboard
        if request.user.role == User.ALFISSEN:
            return redirect('core:alfissen_dashboard')
        else:
            return redirect('core:ouakkaha_dashboard')
    else:
        # Admin goes to order detail
        return redirect('orders:order_detail', order.id)
