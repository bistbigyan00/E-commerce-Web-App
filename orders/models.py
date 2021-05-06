from django.db import models

from ecommerce.utils import *
from django.db.models.signals import pre_save,post_save
from carts.models import Cart
from billing.models import BillingProfile
from addresses.models import Address

#this is to give choices to admin via dropdown of order status
ORDER_STATUS_CHOICES = (
    ('created','created'),
    ('paid','paid'),
    ('shipped','shipped'),
    ('refunded','refunded')
)

class OrderManager(models.Manager):

    def new_or_get(self,billing_profile,cart_obj):
        #if there is already order
        created = False
        qs = Order.objects.filter(billing_profile=billing_profile,cart=cart_obj,active=True)
        if qs.count() == 1:
            obj = qs.first()
        else:
            #using signal in order, old orders with same cart id is already set to false before creating
            #and create new order with same cart
            obj = Order.objects.create(billing_profile=billing_profile,cart=cart_obj,active=True)
            created = True

        return obj, created

# Create your models here.
class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE,null=True,blank=True)
    order_id        =   models.CharField(max_length=120,blank=True)
    shipping_address=   models.ForeignKey(Address,related_name='shippping_address',null=True,blank=True, on_delete = models.CASCADE)
    billing_address =   models.ForeignKey(Address,related_name='billing_address',null=True,blank=True,on_delete=models.CASCADE)
    cart            =   models.ForeignKey(Cart,on_delete=models.CASCADE)
    status          =   models.CharField(max_length=120,default='created',choices=ORDER_STATUS_CHOICES)
    shipping_total  =   models.DecimalField(default=5.99,max_digits=100,decimal_places=2)
    total           =   models.DecimalField(default=0.00,max_digits=100,decimal_places=2)
    active          =   models.BooleanField(default=True)

    objects = OrderManager()

    def __str__(self):
        return self.order_id

    #this method can be used instead of signals
    """def save(self,*args,**kwargs):
        self.total = self.shipping_total + self.cart.total
        super().save(*args,**kwargs)"""

    #method to save the total and update
    def update_total(self):
        shipping_total = self.shipping_total
        cart_total = self.cart.total
        new_total = float(shipping_total) + float(cart_total)
        self.total = new_total
        self.save()
        #always a variable need to be returned instead of self.total
        return new_total

    def check_done(self):
        billing_profile = self.billing_profile
        billing_address = self.billing_address
        shipping_address = self.shipping_address
        total=self.total
        if billing_profile and shipping_address and billing_address and total > 0:
            return True
        return False

    def mark_paid(self):
        if self.check_done():
            self.status = "paid"
            self.save()
        return self.status

#signal for creating unique order id before saving
def pre_save_order_id_receiver(instance,sender,*args,**kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

    #when guest did create order, it was his email address, but if he logs in, then new billing profile is created so, we set old order to False
    #when new order is created, then old order of same cart id whould be set to False
    qs = Order.objects.exclude(billing_profile=instance.billing_profile).filter(cart=instance.cart)
    if qs.exists():
        qs.update(active=False)

pre_save.connect(pre_save_order_id_receiver,sender=Order)

""" VViP
    In order to see the changes in database, please refersh the admin link which uh are using
    if, product is updated in cart, then refresh order link to see the price changes
"""

#if user wants to change the cart,after saving
def post_save_cart_total_receiver(sender,instance,created,*args,**kwargs):
    #check if order is already created or not
    if not created:
        print('not new')
        cart_obj = instance #as sender is Cart so instance is the object of Sender
        cart_id = cart_obj.id
        #get the order of the selected cart
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()  #although there is only one query return but filter retuns in a list
            #although update_total is a fucntion but its still like a field of Model
            order_obj.update_total()

post_save.connect(post_save_cart_total_receiver,sender=Cart)

#signals when Cart is finalised and we just have to create the order total
#this works just for once if cart wont be changed again
def post_save_total_receiver(sender,instance,created,*args,**kwargs):
    if created:
        instance.update_total()

post_save.connect(post_save_total_receiver,sender=Order)
