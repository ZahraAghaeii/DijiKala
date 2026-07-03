"""
URL configuration for DijiKala project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from marketplace.views import (
    home_view, stores_view, store_detail_view, 
    seller_panel_view, customer_panel_view, cart_view, payment_view,
    login_view, logout_view, signup_view, create_store_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('stores/', stores_view, name='stores'),
    path('stores/<int:store_id>/', store_detail_view, name='store_detail'),
    path('seller/', seller_panel_view, name='seller_panel'),
    path('customer/', customer_panel_view, name='customer_panel'),
    path('cart/', cart_view, name='cart'),
    path('payment/', payment_view, name='payment'),
    
    # مسیرهای احراز هویت و ساخت فروشگاه برای هماهنگی با ناوبری base.html
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('create-store/', create_store_view, name='create_store'),
]