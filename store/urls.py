
from django.urls import path
from . import views
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

app_name = 'store'

urlpatterns = [
    path('login/',views.loginUser,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('signup/',views.signUpUser,name="sign_up"),
    path('',views.home,name="home"),
    path('product_id=<str:pk>/',views.productView,name="product_view"),
    path('category/category_id=<str:pk>/',views.categoryView,name="category_view"),
    path('product/search=<str:searchtext>/',views.searchProduct,name="search_product"),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('update_item/',views.updateItem, name="update_item"),
    path('process_order/',views.processOrder, name="process_order"),
]