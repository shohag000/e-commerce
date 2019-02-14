"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import get_login,get_logout,get_register,guest_register_view
from ecommerce.views import home_view
from addresses.views import checkout_address_create_view,checkout_address_reuse_view
from carts.views import cart_home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',home_view,name='home'),
    path('login/',get_login,name='login'),
    path('register/',get_register,name='register'),
    path('register/guest',guest_register_view,name='guest_register'),
    path('checkout/address/create/',checkout_address_create_view,name='checkout_address_create'),

    path('checkout/address/reuse/', checkout_address_reuse_view, name='checkout_address_reuse'),

    #path('cart/',cart_home,name='cart'),
    path('logout/',get_logout,name='logout'),
    path('products/', include(('products.urls','products'),namespace='products')),
    path('', include(('search.urls','search'),namespace='search')),
    path('cart/', include(('carts.urls','carts'),namespace='cart'))


]

if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL,document_root= settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)