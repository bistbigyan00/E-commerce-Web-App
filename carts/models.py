from django.db import models
from django.conf import settings
from django.db.models.signals import m2m_changed,pre_save,post_save

User = settings.AUTH_USER_MODEL

from products.models import Product

#creating model manager
class CartManager(models.Manager):

    def new(self,user=None):
        #create a cart with user or none
        #check if user is there and authenticated
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                #left user is just variable
                #right user is logged in user sent via views with request.user
                user_obj = user

        return self.model.objects.create(user=user_obj)

    #if cart is not create cart, if cart is, but no user, then create user,
    #if cart and user, then get that cart
    def new_or_get(self,request):
        #get the cart id if there is, or set to None
        cart_id = request.session.get('cart_id',None)
        #get cart object with that cart id
        qs = self.get_queryset().filter(id=cart_id)
        if qs.exists():
            new_obj = False
            cart_obj = qs.first()
            if cart_obj.user is None and request.user.is_authenticated:
                cart_obj.user = request.user
                cart_obj.save()

        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            #set the session
            request.session['cart_id'] = cart_obj.id

        return cart_obj,new_obj

# Create your models here.
class Cart(models.Model):
    user    = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products= models.ManyToManyField(Product, blank=True)
    subtotal   = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total   = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    #creating the objects of model manager
    objects = CartManager()

    def __str__(self):
        return str(self.id)

#creating signal to calculate the price of products in the cart
def m2m_changed__cart_receiver(instance,sender, action,*args,**kwargs):
    #this is from documentation
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        #get all the products from cart
        products = instance.products.all()
        total = 0
        for product in products:
            total += product.price
            if instance.subtotal != total:
                #if both are same then, we will not save
                #subtotal is like changing according to products
                #total is like total amount all together
                instance.subtotal = total
                #save to cart with total
                instance.save()

#above we do save() because it doesnot save automatically
m2m_changed.connect(m2m_changed__cart_receiver,sender=Cart.products.through)

#signals for saving Cart
def pre_save_cart_receiver(instance,sender,*args,**kwargs):
    #here we can use 10% vat
    instance.total = float(instance.subtotal) * float(1.08)

pre_save.connect(pre_save_cart_receiver,sender=Cart)
