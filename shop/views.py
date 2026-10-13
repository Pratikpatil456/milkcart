from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from .models import Product, CartItem, Customer, OrderPlaced, Wishlist


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect('cart')


@login_required
def cart(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in items)
    return render(request, 'cart.html', {'items': items, 'total': total})


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart')


@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user)
    if not items:
        messages.warning(request, "Your cart is empty.")
        return redirect('home')

    if request.method == 'POST':
        name = request.POST.get('name')
        locality = request.POST.get('locality')
        city = request.POST.get('city')
        mobile = request.POST.get('mobile')
        zipcode = request.POST.get('zipcode')
        state = request.POST.get('state')

        customer, _ = Customer.objects.get_or_create(
            user=request.user,
            defaults={
                'name': name, 'locality': locality, 'city': city,
                'mobile': mobile, 'zipcode': zipcode, 'state': state,
            }
        )

        for item in items:
            OrderPlaced.objects.create(
                user=request.user,
                customer=customer,
                product=item.product,
                quantity=item.quantity,
            )

        items.delete()
        messages.success(request, "Order placed successfully!")
        return redirect('orders')

    total = sum(item.total_price() for item in items)
    return render(request, 'checkout.html', {'items': items, 'total': total})


@login_required
def orders(request):
    user_orders = OrderPlaced.objects.filter(user=request.user).order_by('-ordered_date')
    return render(request, 'orders.html', {'orders': user_orders})


@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'items': items})


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist')