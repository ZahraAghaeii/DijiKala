from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Store, CartItem, CustomerProfile, SellerProfile, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from decimal import Decimal
from .forms import CustomSignupForm

# صفحه اصلی
def home_view(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'products': products})

# صفحه لیست فروشگاه‌ها
def stores_view(request):
    stores = Store.objects.all()
    return render(request, 'stores.html', {'stores': stores})

# صفحه جزئیات فروشگاه
def store_detail_view(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    products = Product.objects.filter(store=store)
    
    context = {
        'store': store,
        'products': products
    }
    return render(request, 'store_detail.html', context)

# پنل فروشنده
@login_required
def seller_panel_view(request):
    seller, _ = SellerProfile.objects.get_or_create(user=request.user)
    stores = Store.objects.filter(owner=seller)
    
    return render(request, 'seller_panel.html', {'stores': stores})

# پنل مشتری
@login_required
def customer_panel_view(request):
    customer, _ = CustomerProfile.objects.get_or_create(user=request.user)
    orders = Order.objects.filter(customer=customer).order_by('-date')
    
    context = {
        'customer': customer,
        'orders': orders
    }
    return render(request, 'customer_panel.html', context)

#  صفحه سبد خرید
@login_required
def cart_view(request):
    customer, _ = CustomerProfile.objects.get_or_create(user=request.user)
    
    cart_items = CartItem.objects.filter(customer=customer)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)

# ویوی افزودن به سبد خرید
@login_required
def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    customer, _ = CustomerProfile.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        customer=customer,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        
    return redirect('cart')

# ویوی حذف آیتم از سبد خرید
@login_required
def remove_from_cart_view(request, item_id):
    customer = get_object_or_404(CustomerProfile, user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, customer=customer)
    
    cart_item.delete() 
    return redirect('cart')


# صفحه پرداخت 
@login_required
def payment_view(request):
    customer, _ = CustomerProfile.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(customer=customer)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    if request.method == 'POST' and 'amount' in request.POST:
        amount_str = request.POST.get('amount', '0')
        if amount_str:
            amount = Decimal(amount_str)
            customer.balance += amount
            customer.save()
        return redirect('checkout')
    
    context = {
        'customer': customer,
        'cart_items': cart_items,
        'total_price': total_price,
        'sufficient_balance': customer.balance >= total_price 
    }
    return render(request, 'payment.html', context)



def login_view(request):
    return render(request, 'registration/login.html')

def logout_view(request):
    return render(request, 'registration/logged_out.html')


def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST) 
        if form.is_valid():
            user = form.save()
            role = request.POST.get('role') 
            phone_number = form.cleaned_data.get('phone') 
            
            if role == 'seller':
                SellerProfile.objects.create(user=user)
            else:
                CustomerProfile.objects.create(user=user, phone=phone_number)
                
            login(request, user)
            return redirect('home')
    else:
        form = CustomSignupForm() 
    return render(request, 'registration/signup.html', {'form': form})

# ساخت فروشگاه جدید
@login_required
def create_store_view(request):
    seller, _ = SellerProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name:
            Store.objects.create(name=name, owner=seller, description=description)
            return redirect('seller_panel')
            
    return render(request, 'seller_panel.html')

# اضافه کردن محصول به فروشگاه
@login_required
def add_product_view(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    seller, _ = SellerProfile.objects.get_or_create(user=request.user)
    
    if store.owner != seller:
        return redirect('home')
        
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image') 
        
        if name and price:
            Product.objects.create(
                name=name,
                price=Decimal(price),
                description=description,
                image=image,
                store=store
            )
            return redirect('store_detail', store_id=store.id)
            
    return redirect('store_detail', store_id=store.id)

# ویوی نهایی کردن خرید و ثبت در تاریخچه سفارشات
@login_required
def checkout_view(request):
    customer, _ = CustomerProfile.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(customer=customer)
    
    if not cart_items.exists():
        return redirect('cart')
        
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    if customer.balance >= total_price:
        
        customer.balance -= total_price
        customer.save()
        
        order = Order.objects.create(customer=customer, total_amount=total_price)
        
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            
            store = item.product.store
            store.balance += (item.product.price * item.quantity)
            store.save()
            
        cart_items.delete() 
        
        return redirect('customer_panel') 
    else:
        return redirect('payment')
        
# ویوی نمایش تاریخچه سفارشات
@login_required
def order_history_view(request):
    customer, _ = CustomerProfile.objects.get_or_create(user=request.user)
    
    orders = Order.objects.filter(customer=customer).order_by('-date')
    
    return render(request, 'order_history.html', {'orders': orders})

# ویوی برای افزایش موجودی کیف پول 
@login_required
def deposit_wallet_view(request):
    if request.method == 'POST':
        amount_str = request.POST.get('amount')
        if amount_str:
            amount = Decimal(amount_str)
            if amount > 0:
                customer, _ = CustomerProfile.objects.get_or_create(user=request.user)
                customer.balance += amount
                customer.save()
                messages.success(request, f"Wallet successfully charged by ${amount}!")
            else:
                messages.error(request, "Invalid amount.")
            
    return redirect(request.META.get('HTTP_REFERER', 'cart'))
