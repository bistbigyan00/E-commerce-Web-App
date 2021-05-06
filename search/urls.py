from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('search/',views.SearchProductView.as_view(),name='query')
]
