from django.contrib import admin
from django.urls import path
from kaaya_login.views import KaayaaLoginUser,Profile,Logout
from kaaya_products.views import ProductsView,CategoryView
from kaayaa_vendor.views import VendorRegisterView
from kaayaa_admin.views import AllVendorView, AllAdminView
from kaayaa_user.views import UserRegisterView, CartOperations
from kaaya_login.refreshToken import MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', KaayaaLoginUser.as_view()),
    path('profile/', Profile.as_view()),
    path('products/', ProductsView.as_view()),
    path('category/', CategoryView.as_view()),
    path('register_vendor/', VendorRegisterView.as_view()),
    path('all_vendor_data/', AllVendorView.as_view()),
    path('refreshToken/',MyTokenObtainPairView.as_view()),
    
    # admin
    path("add-admin/", AllAdminView.as_view()),
    
    # User
    path('add-user/', UserRegisterView.as_view()),
    
    # Cart
    path('add-to-cart/', CartOperations.as_view()),
    path('update-cart/<int:cart_id>', CartOperations.as_view()),
]
