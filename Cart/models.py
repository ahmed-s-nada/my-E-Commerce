from django.db import models
from django.conf import settings
from Product.models import Product
from decimal import Decimal
from django.db.models.signals import m2m_changed, pre_save, post_save, pre_delete, post_delete
# Create your models here.

User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):

    def get_or_create_cart(self, request):
        # request.session = None
        cart__id = request.session.get('cart__id', None)
        current_user = request.user

        if current_user.is_authenticated:
            user_cart_qs = Cart.objects.filter(user = current_user)
            if user_cart_qs.count() == 1:
                cart_obj = user_cart_qs.first()
                request.session['cart__id'] = cart_obj.id
                new_cart_flag = False
            else:
                if cart__id is None:
                    cart_obj = Cart.objects.create(user = current_user)
                    request.session['cart__id'] = cart_obj.id
                    new_cart_flag = True
                else:
                    cart_qs = Cart.objects.filter(id = cart__id)
                    cart_obj = cart_qs.first()
                    cart_obj.user = current_user
                    cart_obj.save()
                    new_cart_flag = False
        else:
            if cart__id is None:
                cart_obj = Cart.objects.create(user = None)
                request.session['cart__id'] = cart_obj.id
                new_cart_flag = True
            else:
                cart_qs = Cart.objects.filter(id = cart__id)
                cart_obj = cart_qs.first()
                new_cart_flag = False

        return cart_obj, new_cart_flag




    def new(self, user=None, products=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return Cart.objects.create(user = user_obj)



class Cart(models.Model):
    user      = models.OneToOneField(User, null = True, blank = True, on_delete=models.CASCADE)
    products  = models.ManyToManyField(Product, blank = True )
    subtotal  = models.DecimalField(decimal_places=2, max_digits=9, default = 0.00)
    taxs      = models.DecimalField(decimal_places=3, max_digits=4, default = 0.10)
    total     = models.DecimalField(decimal_places=2, max_digits=9, default = 0.00)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True)

    objects= CartManager()

    def __str__(self):
        return str(self.id)


def cart_m2m_reciever(instance, sender, action, *args, **kwargs):
    if action == "post_add" or action == "post_remove" or action == "post_clear" :
        products = instance.products.all()
        the_sum = 0
        for p in products:
            the_sum += p.price
        instance.subtotal = the_sum
        instance.save()

m2m_changed.connect(cart_m2m_reciever, sender=Cart.products.through) #<== Notice how many to many sender should be


def cart_pre_save_reciever(instance, sender, *args, **kwargs):
    # instance.total = instance.subtotal + (Decimal(instance.subtotal) * Decimal(instance.taxs))
    instance.total = instance.subtotal
    
pre_save.connect(cart_pre_save_reciever, sender=Cart)
