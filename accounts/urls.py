from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/',views.login_page,name='login'),
    path('guest_checkout/',views.guest_page_view,name='guest_checkout'),
    path('register/',views.register_page,name='register'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
]
