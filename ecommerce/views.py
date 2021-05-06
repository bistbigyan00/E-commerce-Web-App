from django.shortcuts import render
from .forms import *
from django.http import JsonResponse

def home(request):
    #print(request.session.get('first_name','Unknown')) #getter
    context = {}
    return render(request,'home.html',context)

def contact(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        'form':contact_form
    }
    if contact_form.is_valid():
        if request.is_ajax():
            console.log(csrf_token)
            return JsonResponse({'message':'Thank You for your submission'})

    return render(request,'contact.html',context)
