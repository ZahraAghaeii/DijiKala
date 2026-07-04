from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Store, CartItem, CustomerProfile
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
def seller_panel_view(request):
    return render(request, 'seller_panel.html')

# ۵. پنل مشتری
def customer_panel_view(request):
    return render(request, 'customer_panel.html')

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
            user = form.save() # ذخیره کاربر جدید در دیتابیس
            login(request, user) # لاگین خودکار بعد از ثبت‌نام موفق
            return redirect('home') # هدایت به صفحه اصلی
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def create_store_view(request):
    return render(request, 'store_detail.html') # یا هر قالبی که بعداً کامل 

# ویوی موقت برای صفحه افزودن محصول جدید
def add_product_view(request, store_id):
    return render(request, 'store_detail.html')  # فعلاً برای رفع ارور، به همین صفحه رندر می‌کنیم

# ویوی نهایی کردن خرید و خالی کردن سبد خرید
@login_required
def checkout_view(request):
    customer, _ = CustomerProfile.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(customer=customer)
    
    if not cart_items.exists():
        return redirect('cart')
        
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    # بررسی کافی بودن موجودی کاربر
    if customer.balance >= total_price:
        # ۱. کسر از موجودی مشتری
        customer.balance -= total_price
        customer.save()
        
        # ۲. منطق دمو برای اضافه کردن به موجودی فروشگاه‌ها (در صورت وجود فیلد balance در مدل Store)
        for item in cart_items:
            store = item.product.store
            if hasattr(store, 'balance'):
                store.balance += item.product.price * item.quantity
                store.save()
        
        # ۳. حذف آیتم‌ها از سبد خرید (خالی کردن سبد)
        cart_items.delete()
        
        # هدایت به یک صفحه یا پیام موفقیت‌آمیز (مثلاً صفحه اصلی یا پنل مشتری)
        return redirect('customer_panel') 
    else:
        # اگر موجودی کافی نبود، هدایت به صفحه پرداخت برای افزایش موجودی
        return redirect('payment')