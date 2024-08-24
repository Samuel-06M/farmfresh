from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .forms import UserRegisterForm, LoginForm, ProductForm
from .models import Product, Cart, CartProduct
from django.http import HttpResponseRedirect

def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'poultrypalace/index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_type = form.cleaned_data.get('user_type')  # Assuming you have a field named 'user_type' in your form
            if user_type == 'farmer':
                user.is_farmer = True
            elif user_type == 'customer':
                user.is_customer = True
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Registration successful! Welcome, {username}!')
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserRegisterForm()
    return render(request, 'poultrypalace/register.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_farmer:
        products = Product.objects.filter(farmer=request.user)
        return render(request, 'poultrypalace/dashboard.html', {'products': products})
    else:
        products = Product.objects.all()
        return render(request, 'poultrypalace/dashboard.html', {'products': products})

@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)
    if created:
        cart_product.quantity = quantity
    else:
        cart_product.quantity += quantity
    cart_product.save()

    messages.success(request, f"Added {product.name} to your cart.")
    return redirect('view_products')

@login_required
def remove_from_cart(request, cart_product_id):
    cart_product = get_object_or_404(CartProduct, id=cart_product_id)
    cart_product.delete()
    messages.success(request, f'Removed {cart_product.product.name} from your cart.')
    return redirect('cart')

@login_required
def view_products(request):
    if request.user.is_farmer:
        products = Product.objects.filter(farmer=request.user)
    else:
        products = Product.objects.all()
    return render(request, 'poultrypalace/view_products.html', {'products': products})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'poultrypalace/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('index')

@login_required
def post_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = request.user
            product.save()
            messages.success(request, "Product posted successfully!")
            return redirect('dashboard')
    else:
        form = ProductForm()
    return render(request, 'poultrypalace/post_product.html', {'form': form})

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart.cartproduct_set.all())
    return render(request, 'poultrypalace/cart.html', {'cart': cart, 'total_price': total_price})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'poultrypalace/edit_product.html', {'form': form})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, farmer=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('view_products')
    return render(request, 'poultrypalace/delete_product.html', {'product': product})

