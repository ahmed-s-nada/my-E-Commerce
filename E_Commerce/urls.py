"""E_Commerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import Home, Contact, RegisterView, LoginView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', Home.as_view(), name = 'Home'),
    path('contact/', Contact.as_view(), name = 'Contact'),
    path('register/',RegisterView.as_view(), name = 'Register'),
    path('login/', LoginView.as_view(), name = 'Login'),
    path('product/', include('Product.urls', namespace = 'Product')),
    path('search/', include('Search.urls', namespace = 'Search')),
    path('cart/', include('Cart.urls', namespace = 'Cart')),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
admin.site.site_header = "Nada's E-Shop admin area"
admin.site.site_title  = "Nada's Eshop"
