from django.urls import path
from .views import (
    add_to_cart_view, cart_view, checkout_view, compare_prices_view, 
    home_view, login_view, register_view, logout_view, orders_view, 
    update_cart_view, remove_from_cart_view, verify_email_view, 
    resend_verification_code_view
)

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('verify-email/', verify_email_view, name='verify_email'),
    path('resend-verification-code/', resend_verification_code_view, name='resend_verification_code'),
    path('logout/', logout_view, name='logout'),
    path('add-to-cart/<int:product_id>/', add_to_cart_view, name='add_to_cart'),
    path('cart/', cart_view, name='cart'),
    path('cart/update/<int:product_id>/', update_cart_view, name='update_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart_view, name='remove_from_cart'),
    path('compare-prices/', compare_prices_view, name='compare_prices'),
    path('checkout/', checkout_view, name='checkout'),
    path('orders/', orders_view, name='orders'),
]