from django.urls import path
from . import views

app_name = 'carts'

urlpatterns = [
    path('carts/',views.cart_home,name='cart'),
    path('cart_update/',views.cart_update,name='cart_update'),
    path('checkout/',views.checkout,name='checkout'),
    path('checkout/done',views.checkout_done_view,name='checkout_done'),
    path('api/cart/',views.api_cart_remove_view,name='api_cart_remove')

]
