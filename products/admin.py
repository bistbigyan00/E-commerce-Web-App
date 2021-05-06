from django.contrib import admin

from .models import *

#to display the slug
class ProductAdmin(admin.ModelAdmin):
    #display the columns
    list_display = ['__str__','slug']
    class Meta:
        model = Product

# Register your models here.
admin.site.register(Product,ProductAdmin)
