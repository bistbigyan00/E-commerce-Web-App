from django.urls import reverse_lazy
from .forms import *

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate,login,get_user_model,logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,FormView,DetailView

from django.shortcuts import render,redirect
from django.utils.http import is_safe_url

from .models import *
from .signals import *

User = get_user_model()

@login_required
def account_home_view(request):
    return render(request,"accounts/home.html",{})

class AccountHomeView(LoginRequiredMixin,DetailView):
    template_name = 'accounts/home.html'

    def get_object(self):
        return self.request.user

class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'

    def get_form_kwargs(self):
        kwargs = super(LoginView,self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_next_url(self):
        request     = self.request
        next_       = request.GET.get('next')
        next_post   = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if is_safe_url(redirect_path,request.get_host()):
            return redirect_path
        return "/"

    def form_valid(self,form):
        next_path = self.get_next_url()
        return redirect(next_path)

class GuestRegisterView(FormView):
    form_class = GuestForm

    def get_next_url(self):
        request     = self.request
        next_       = request.GET.get('next')
        next_post   = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if is_safe_url(redirect_path,request.get_host()):
            return redirect_path
        return 'accounts/register'

    def form_valid(self,form):
        request     = self.request
        email       = form.cleaned_data['email']
        guest       = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = guest.id

        next_path   = self.get_next_url()
        return redirect(next_path)



def guest_page_view(request):
    form = GuestForm(request.POST or None)

    next_ = request.GET.get('next')
    next_url = request.POST.get('next')
    redirect_path = next_ or next_url
    print('guest')
    print(redirect_path)

    if form.is_valid():
        email = form.cleaned_data['email']
        guest = GuestEmail.objects.create(email=email)

        request.session['guest_email_id'] = guest.id

        if is_safe_url(redirect_path,request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('accounts/register')

    return redirect('accounts/register')

class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy("accounts:login")
    template_name = "accounts/register.html"
