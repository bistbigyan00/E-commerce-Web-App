from django.shortcuts import render
from products.models import Product
from django.views.generic import ListView

# Create your views here.
class SearchProductView(ListView):
    template_name = 'search/view.html'

    def get_queryset(self,*args,**kwargs):
        request = self.request
        #use GET method from the submit value
        method_dict = request.GET
        #store the item from
        search_item = method_dict.get('q',None)

        if search_item is not None:
            return Product.objects.search(search_item)
        #displays if nothing is searched or matched
        return Product.objects.featured()

    def get_context_data(self,*args,**kwargs):
        #general inheritance
        context = super(SearchProductView,self).get_context_data(*args,**kwargs)
        #setting value to query with input searched item
        context['query'] = self.request.GET.get('q')

        return context
