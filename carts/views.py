from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from accounts.forms import LoginForm,GuestForm
from addresses.forms import AddressForm

from .models import Cart
from orders.models import Order
from products.models import Product
from billing.models import BillingProfile
from accounts.models import GuestEmail
from addresses.models import Address

#importing stripe key
import stripe
stripe.api_key = "sk_test_51IiZrxKWI8M2i0OA25Ei7UFoIxtV3g23VSn3MWurpHOefiAvwHRVy0QwSPJjSy2qwok8mH06Qo9ZUXLaiDPNjcP200JDz95LFB"

def api_cart_remove_view(request):
    cart_obj,new_obj = Cart.objects.new_or_get(request)
    products = cart_obj.products.all()

    #json only take data in form of dictionary so we convert products detail into dictionary
    products = [
        {
            'id':product.id,
            'url':product.get_absolute_url(),
            'name':product.title,
            'price':product.price
        }
        for product in products
    ]

    #send json response to data, which data need to be refresh via ajax
    cart_data = {
        'product':products,
        'subtotal':cart_obj.subtotal,
        'total':cart_obj.total
        }
    return JsonResponse(cart_data)

# Create your views here.
def cart_home(request):
    #using model Manager
    #so that we can use the cart_obj anywhere if we need to use that session id
    cart_obj, new_obj = Cart.objects.new_or_get(request)

    return render(request,'carts/home.html',{'cart':cart_obj})

def cart_update(request):
    #receive id from POST method using form
    product_id = request.POST['product_id']
    product = Product.objects.get(id=product_id)
    #getting card or creating if not
    cart_obj,new_obj = Cart.objects.new_or_get(request)

    #check if product is alreay in there:
    if product in cart_obj.products.all():
        cart_obj.products.remove(product)
        added = False
    else:
        #adding received product to cart
        cart_obj.products.add(product)
        added = True
        #as we want to see cart items total in everypage so we store in session and displays in navbar
    request.session['cart_items'] = cart_obj.products.count()

    #if data is sent via ajax
    if request.is_ajax():
        json_data = {
            'added':added,
            'removed':not added,
            'cartProductCount':cart_obj.products.count(),
        }
        return JsonResponse(json_data)

    return redirect ('carts:cart')

def checkout(request):
    #new_obj is boolean field
    #these none we have to create because error will pop up as it is passes via context
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect('carts:cart')

    login_form = LoginForm(request=request)
    guest_form = GuestForm()
    address_form = AddressForm()

    billing_address_id = request.session.get("billing_address_id",None)
    shipping_address_id = request.session.get("shipping_address_id",None)

    #creating billing profile using model Manager
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    #behind the scene we need to create the order, on the basis of billing profile, cart and set that order to true
    #here definitely there is billing profile from above
    #order is created using model manager
    address_qs = None
    if billing_profile is not None:

        #get the address detail of same billing profile
        address_qs = Address.objects.filter(billing_profile=billing_profile)

        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile,cart_obj)

        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
        if shipping_address_id or billing_address_id:
            order_obj.save()

    if request.method == 'POST':

        if order_obj.check_done():
            order_obj.mark_paid()
            print(order_obj.mark_paid())
            request.session['cart_items']=0
            del request.session['cart_id']
            return redirect('carts:checkout_done')


    context = {
        'object':order_obj,
        'billing_profile':billing_profile,
        'login_form':login_form,
        'guest_form':guest_form,
        'next_url':request.build_absolute_uri,
        'address_form':address_form,
        'address_qs':address_qs
    }

    return render(request,'carts/checkout.html',context)


def checkout_done_view(request):
    return render(request,'carts/checkout_done.html',{})
