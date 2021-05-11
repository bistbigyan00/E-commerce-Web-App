from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/',views.LoginView.as_view(),name='login'),
    path('guest_checkout/',views.GuestRegisterView.as_view(),name='guest_checkout'),
    path('register/',views.SignUp.as_view(),name='register'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('accounts/',views.AccountHomeView.as_view(),name='home')

]
