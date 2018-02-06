from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View, RedirectView,ListView
from .models import Cart
from Product.models import Product
from Invoice.models import Invoice

# Create your views here.

class CartHome(TemplateView):

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(CartHome, self).get_context_data(**kwargs)
        context['items'] = kwargs['items']
        context['total'] = str(kwargs['total']) + ' EGP'
        context['id'] = kwargs['cart__id']
        return context


    def get(self, request, *args, **kwargs):

        cart_obj, new_cart_flag = Cart.objects.get_or_create_cart(request)
        cart__id = cart_obj.id
        sub_total= cart_obj.subtotal
        items    = cart_obj.products.all()
        names    = [x.name for x in cart_obj.products.all()]
        prices   = [x.price for x in cart_obj.products.all()]
        total    = cart_obj.total


        return render(request, 'home.html', self.get_context_data(cart__id = cart__id,
                                                                  items =  items, total= total,
                                                                  sub_total = sub_total))




class CartUpdate(TemplateView):  # Addin and Removing objects to and fromthe cart

    template_name = 'home.html'

    def post(self, request, *args, **kwargs): # <== Using POST method in the template and overriding
        # print (request.POST)                #     It here to get request and the variable 'product_id'
        cart_obj, new_cart_flag = Cart.objects.get_or_create_cart(request)
        cart__id                = cart_obj.id
        product_id              = request.POST.get('product_id')
        the_product             = Product.objects.my_get_by_id (product_id)
        if not the_product in cart_obj.products.all():
            cart_obj.products.add(the_product)  # <== This is how to add object to ManyToManyField
        else:
            cart_obj.products.remove(the_product)
        product_list            = cart_obj.products.all()
        # prices                  = [x.price for x in cart_obj.products.all()]
        total                   = cart_obj.total

        return redirect('Cart:CarrtHome')


class InvoiceHome(TemplateView):
        template_name = 'home.html'
        def post(self, request, *args, **kwargs):
            cart_obj, new_cart_flag = Cart.objects.get_or_create_cart(request)
            Invoice.objects.new(request, cart_obj)
            return redirect('Home')
