from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Store, CartItem, CustomerProfile, SellerProfile, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from decimal import Decimal

def home_view(request):
    # گرفتن همه محصولات و مرتب‌سازی بر اساس جدیدترین‌ها
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'products': products})

# ۲. صفحه لیست فروشگاه‌ها
def stores_view(request):
    stores = Store.objects.all()  # گرفتن تمام فروشگاه‌ها از دیتابیس
    return render(request, 'stores.html', {'stores': stores})

# ۳. صفحه جزئیات فروشگاه
def store_detail_view(request, store_id):
    # پیدا کردن فروشگاه بر اساس آی‌دی، اگر نبود ارور 404 می‌دهد
    store = get_object_or_404(Store, id=store_id)
    # پیدا کردن تمام محصولات متعلق به این فروشگاه
    products = Product.objects.filter(store=store)
    
    context = {
        'store': store,
        'products': products
    }
    return render(request, 'store_detail.html', context)

# ۴. پنل فروشنده
@login_required
def seller_panel_view(request):
    # دریافت یا ساخت پروفایل فروشنده
    seller, _ = SellerProfile.objects.get_or_create(user=request.user)
    # دریافت فروشگاه‌های متعلق به این فروشگاه
    stores = Store.objects.filter(owner=seller)
    
    return render(request, 'seller_panel.html', {'stores': stores})

# ۵. پنل مشتری
@login_required
def customer_panel_view(request):
    # دریافت یا ساخت پروفایل مشتری
    customer, _ = CustomerProfile.objects.get_or_create(user=request.user)
    # دریافت سفارشات قبلی کاربر برای بخش تاریخچه سفارشات
    orders = Order.objects.filter(customer=customer).order_by('-date')
    
    context = {
        'customer': customer,
        'orders': orders
    }
    return render(request, 'customer_panel.html', context)

# ۶. صفحه سبد خرید
@login_required
def cart_view(request):
    # اگر پروفایل مشتری وجود نداشت، خودش خودکار یکی می‌سازد (get_or_create)
    customer, _ = CustomerProfile.objects.get_or_create(user=request.user)
    
    cart_items = CartItem.objects.filter(customer=customer)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)

# ویوی هوشمند افزودن به سبد خرید
@login_required
def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # اگر پروفایل مشتری وجود نداشت، خودش خودکار یکی می‌سازد تا ارور 404 ندهد
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
    # پیدا کردن آیتم سبد خرید بر اساس آی‌دی که متعلق به همین کاربر باشد
    customer = get_object_or_404(CustomerProfile, user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, customer=customer)
    
    cart_item.delete() # حذف آیتم از دیتابیس
    return redirect('cart') # ریدایرکت مجدد به صفحه سبد خرید


# ۷. صفحه پرداخت آزمایشی
@login_required
def payment_view(request):
    customer, _ = CustomerProfile.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(customer=customer)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    if request.method == 'POST' and 'amount' in request.POST:
        # تبدیل ورودی به Decimal به جای float برای هماهنگی با دیتابیس
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

# ویوهای موقت برای احراز هویت و ساخت فروشگاه
def login_view(request):
    return render(request, 'registration/login.html')

def logout_view(request):
    return render(request, 'registration/logged_out.html')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = request.POST.get('role')  # دریافت نقش از فرم HTML (customer یا seller)
            
            if role == 'seller':
                SellerProfile.objects.create(user=user)
            else:
                # به صورت پیش‌فرض یا در صورت انتخاب مشتری
                CustomerProfile.objects.create(user=user)
                
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


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

@login_required
def add_product_view(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    seller, _ = SellerProfile.objects.get_or_create(user=request.user)
    
    # امنیت: بررسی اینکه آیا این فروشگاه واقعاً متعلق به کاربر فعلی است یا خیر
    if store.owner != seller:
        return redirect('home')
        
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image') # برای آپلود تصویر اختیاری
        
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

@login_required
def checkout_view(request):
    customer, _ = CustomerProfile.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(customer=customer)
    
    if not cart_items.exists():
        return redirect('cart')
        
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    if customer.balance >= total_price:
        # ۱. کسر از موجودی مشتری
        customer.balance -= total_price
        customer.save()
        
        # ۲. ثبت سفارش اصلی
        order = Order.objects.create(customer=customer, total_amount=total_price)
        
        # ۳. ثبت تک‌تک آیتم‌ها در تاریخچه سفارشات و خالی کردن سبد خرید
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            # (نکته داینامیک داکیومنت: اضافه کردن منطقی به موجودی فرضی فروشگاه در صورت تمایل)
            
        cart_items.delete() # خالی کردن سبد خرید خرید پس از موفقیت
        
        # اگر سیستم تشکر پس از پرداخت (امتیازی) داری، اینجا رندر کن
        return render(request, 'payment.html', {'success': True}) 
    else:
        return redirect('payment') 
    
@login_required
def order_history_view(request):
    # پیدا کردن پروفایل مشتری
    customer, _ = CustomerProfile.objects.get_or_create(user=request.user)
    
    # گرفتن تمام سفارشات این مشتری به همراه آیتم‌های داخل هر سفارش
    orders = Order.objects.filter(customer=customer).order_by('-date')
    
    return render(request, 'order_history.html', {'orders': orders})    