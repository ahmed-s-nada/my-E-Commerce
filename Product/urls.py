from django.urls import path
from Product.views import ProductDetail, ProductList

app_name = 'Product'

urlpatterns = [
    path('', ProductList.as_view(),name = 'List'),
    path('single/<slug:slug>/', ProductDetail.as_view(),name = 'Single'),


]
