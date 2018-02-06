from django.urls import path
from .views import CartHome, CartUpdate, InvoiceHome


app_name = 'Cart'

urlpatterns = [
    path('', CartHome.as_view(), name = 'CarrtHome'),
    path('add/', CartUpdate.as_view(), name = 'Update'),
    path('checkout/', InvoiceHome.as_view(), name ='Checkout')
    # path('advanced/', AdvancedSearch.as_view(), name = 'Advanced'),
    # path('single/<slug:slug>/', ProductDetail.as_view(),name = 'Single'),


]
