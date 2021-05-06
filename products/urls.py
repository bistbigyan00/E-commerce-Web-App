from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'products'

urlpatterns = [
    path('products/',views.ProductListView.as_view(),name='product'),
    path('featured/',views.ProductFeaturedList.as_view(),name='featured'),

    #path('products/<str:pk>/',views.ProductDetailView.as_view()),
    path('featured/<str:pk>/',views.ProductFeaturedDetail.as_view(),name='singleFeatured'),
    path('products/<slug:slug>/',views.ProductDetailSlugView.as_view(),name='singleProduct')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#above code displays files uploaded
