from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from marketplace.views import (
    home_view, stores_view, store_detail_view, 
    seller_panel_view, customer_panel_view, cart_view, payment_view,
    login_view, logout_view, signup_view, create_store_view, add_product_view,
    add_to_cart_view, remove_from_cart_view, checkout_view,
    order_history_view  # این همون تابعی هست که دوستت جدیداً اضافه کرده
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('stores/', stores_view, name='stores'),
    path('stores/<int:store_id>/', store_detail_view, name='store_detail'),
    path('seller/', seller_panel_view, name='seller_panel'),
    path('customer/', customer_panel_view, name='customer_panel'),
    path('cart/', cart_view, name='cart'),
    path('cart/add/<int:product_id>/', add_to_cart_view, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart_view, name='remove_from_cart'),
    
    # بخش پرداخت و چک‌اوت تو
    path('cart/checkout/', checkout_view, name='process_checkout'), 
    path('payment/', checkout_view, name='checkout'), 
    path('payment/process/', payment_view, name='payment'),
    
    # آدرسی که دوستت برای تاریخچه سفارشات ساخته
    path('customer/orders/', order_history_view, name='order_history'),
    
    path('signup/', signup_view, name='signup'),
    path('create-store/', create_store_view, name='create_store'),
    path('stores/<int:store_id>/add-product/', add_product_view, name='add_product'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
