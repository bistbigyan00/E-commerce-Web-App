from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from .forms import *

from billing.models import BillingProfile

def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    context = {
        'form':form
    }
    #as next_url is sent via context which is GET and also sent via form, so from anywhere if it is received it will redirect to same page after action
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    if form.is_valid():
        instance = form.save(commit=False)
        #using model manager of billing

        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

        if billing_profile is not None:
            address_type = request.POST.get('address_type','shipping')

            instance.billing_profile = billing_profile
            instance.address_type = address_type
            instance.save()
            #saving address id into instance, so that we can use this to grab address object in cart
            request.session[address_type + '_address_id'] = instance.id

        else:
            print('Error here')
            return redirect('carts:checkout')

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect(redirect_path)

    return redirect('carts:checkout')


def checkout_address_reuse(request):
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    if request.method == 'POST':
        print(request.POST)
        shipping_address = request.POST.get('shipping_address',None)
        address_type = request.POST.get('address_type','shipping')

        request.session[address_type + "_address_id"] = shipping_address

        if is_safe_url(redirect_path,request.get_host()):
            return redirect(redirect_path)

    return redirect('carts:checkout')
