from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Store, CartItem

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
def cart_view(request):
    # فعلاً برای تست، اقلام سبد خرید را می‌کشیم (بعداً با سیستم یوزرها دقیق‌ترش می‌کنیم)
    cart_items = CartItem.objects.all()
    
    # محاسبه قیمت کل سبد خرید
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)

def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # پیدا کردن یا ساختن آیتم در سبد خرید
    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        
    return redirect('cart')

# ۷. صفحه پرداخت آزمایشی
def payment_view(request):
    return render(request, 'payment.html')

# ویوهای موقت برای احراز هویت و ساخت فروشگاه
def login_view(request):
    return render(request, 'registration/login.html')

def logout_view(request):
    return render(request, 'registration/logged_out.html')

def signup_view(request):
    return render(request, 'registration/signup.html')

def create_store_view(request):
    return render(request, 'store_detail.html') # یا هر قالبی که بعداً کامل 

# ویوی موقت برای صفحه افزودن محصول جدید
def add_product_view(request, store_id):
    return render(request, 'store_detail.html')  # فعلاً برای رفع ارور، به همین صفحه رندر می‌کنیم