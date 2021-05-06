from django.db import models

from products.models import Product
from django.db.models.signals import pre_save,post_save
from ecommerce.utils import unique_slug_generator

# Create your models here.
class Tag(models.Model):
    title       = models.CharField(max_length=120)
    slug        = models.SlugField()
    products    = models.ManyToManyField(Product,blank=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

def tag_pre_save_receiver(instance,sender,*args,**kwargs):
    instance.slug = unique_slug_generator(instance)

pre_save.connect(tag_pre_save_receiver,sender=Tag)