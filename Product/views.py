from django.shortcuts import render
from django.http import Http404
from Product.models import Product
from Product.forms import ProductForm
from django.views.generic import RedirectView, ListView, CreateView, FormView, CreateView, DetailView, DeleteView
from Cart.models import Cart
# Create your views here.


class ProductList(ListView):

    model = Product
    template_name = 'Product/product_list.html'
    context_object_name = 'product_list'
    def get_context_data(self, *args, **kwargs):
        context = super(ProductList, self).get_context_data(*args, **kwargs)
        context['header'] = 'Welcome to our product list!'
        return context




class ProductDetail(DetailView):

    model = Product
    context_object_name = 'single_product'


    def get_context_data(self, **kwargs):
        request = self.request # <= get the requset (VERY IMPORTANT)
        context = super(ProductDetail, self).get_context_data(**kwargs)
        cart_obj, cart_status = Cart.objects.get_or_create_cart(request)
        context['cart'] = cart_obj
        print (cart_obj)
        return context


    def get_object(self, *args, **kwargs): # <== overriding the get_object to put our 404 message
        # request = self.request
        slug = self.kwargs.get('slug')
        instance  = Product.objects.my_get_by_slug(slug = slug)
        if instance is None :
            raise Http404('No such product!')
        # print (instance.images.all())
        return instance
