import random
import os

from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save

from django.db.models import Q

from ecommerce.utils import *

class ProductManager(models.Manager):

    def get_by_id(self,id):
        instance = self.get_queryset().filter(id=id)
        if instance.count() == 1:
            return instance.first()
        return None

    def featured(self):
        return self.get_queryset().filter(featured=True)

    def search(self,query):
        #using lookups and also using related field of many to many using tag and product
        lookups = Q(title__icontains=query)|Q(description__icontains=query)|Q(price__icontains=query)|Q(tag__title__icontains=query)
        return self.get_queryset().filter(lookups).distinct()

# Create your models here.
class Product(models.Model):
    title       = models.CharField(max_length=120)
    slug        = models.SlugField(blank=True,unique=True,allow_unicode=True)
    description = models.TextField()
    price       = models.DecimalField(decimal_places=2,max_digits=10,default=39.99)
    image       = models.FileField(upload_to='products', null=True,blank=True)
    featured    = models.BooleanField(default=False)
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:singleProduct', kwargs={'slug':self.slug})

#this is a signal method receiver
def product_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

#connect this signal method with sender
pre_save.connect(product_pre_save_receiver,sender=Product)
