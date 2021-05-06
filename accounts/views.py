from django.contrib.auth import authenticate,login,get_user_model,logout
from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from .forms import *
from .models import *
from .signals import *

User = get_user_model()

# Create your views here.
def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        'form':form
    }

    next_       = request.GET.get('next')
    next_post   = request.POST.get('next')
    redirect_path = next_ or next_post
    print('login')
    print(redirect_path)
    if form.is_valid():
        #receives username from database
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        #authenticate automatically
        user = authenticate(request,username=username,password=password)
        if user is not None:
            #do the login process
            login(request,user)
            #as soon as login is done, the instance and request is passed to the custom signal
            user_logged_signal.send(user.__class__, instance=user,request=request)
            try:
                del request.session['guest_email_id']
            except:
                pass

            if is_safe_url(redirect_path,request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        else:
            print('Error')
    return render(request,"accounts/login.html",context)

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


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = User.objects.create(username=username,email=email,password=password)
    return render(request,"accounts/register.html",context)
