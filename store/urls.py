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
    path('',views.home,name="home"),
    path('product_id=<str:pk>/',views.productView,name="product_view"),
    path('cart/',views.cart,name="cart"),
    path('update_item/',views.updateItem, name="update_item"),
    path('process_order/',views.processOrder, name="process_order"),
]