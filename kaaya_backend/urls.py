"""kaaya_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from kaaya_login.views import KaayaaLoginUser,Profile
from kaaya_products.views import ProductsView
from kaayaa_vendor.views import VendorRegisterView
from kaayaa_admin.views import AllVendorView
from kaayaa_user.views import UserRegisterView, CartOperations

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', KaayaaLoginUser.as_view()),
    path('profile/', Profile.as_view()),
    path('products/', ProductsView.as_view()),
    path('register_vendor/', VendorRegisterView.as_view()),
    path('all_vendor_data/', AllVendorView.as_view()),
    
    # User
    path('add-user/', UserRegisterView.as_view()),
    
    # Cart
    path('add-to-cart/', CartOperations.as_view()),
]
