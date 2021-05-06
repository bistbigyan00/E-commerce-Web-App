from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.shortcuts import render,get_object_or_404

from analytics.mixins import ObjectViewedMixin

from .models import *
from carts.models import Cart

# Create your views here.
class ProductDetailSlugView(ObjectViewedMixin,DetailView):
    queryset = Product.objects.all()
    template_name = 'products/detail.html'

    def get_context_data(self,*args,**kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args,**kwargs)
        #this new_or_get returns two thing card_obj and new_obj
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self,*args,**kwargs):
        request = self.request
        slug = self.kwargs.get('slug')

        instance = get_object_or_404(Product,slug=slug)
        return instance

class ProductFeaturedList(ListView):
    model = Product
    template_name = 'products/list.html'

    def get_queryset(self,*args,**kwargs):
        return Product.objects.featured()

class ProductFeaturedDetail(ObjectViewedMixin,DetailView):
    queryset = Product.objects.featured()
    template_name = 'products/detail.html'

class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'

class ProductDetailView(ObjectViewedMixin,DetailView):
    queryset = Product.objects.all()
    template_name = 'products/detail.html'

    def get_context_data(self,*args,**kwargs):
        context = super(ProductDetailView,self).get_context_data(*args,**kwargs)
        return context
