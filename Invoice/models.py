from django.db import models
from Cart.models import Cart
from django.db.models.signals import pre_save
import uuid
from datetime import datetime
# Create your models here.

class InvoiceManager(models.Manager):
    def new(self, requset, cart): # <== Creating an invoice based on the active cart
        total = cart.total
        status = 'CREATED'
        created_at = datetime.now
        new_inovice = Invoice.objects.create(cart = cart, total = total, status = status, creation_time = created_at)
        cart.delete()  # <== Removing the cart after the creation of the invoice and finishing the checkout 
        requset.session['cart__id'] = None
        return new_inovice

class Invoice(models.Model):

    STATUS_LIST     = [('CREATED','Created'),('SHIPPED', 'Shipped'),('DELIVERED','Delivered'),('CANCLED', 'Cancel')]

    invoice_id      = models.CharField(max_length = 64, unique = True, editable = False, blank = True)
    # billing_profile =
    buyer           = models.CharField(max_length = 64, blank = True, null = True)
    cart            = models.ForeignKey(Cart, on_delete=models.SET_NULL, null = True )
    shipping        = models.DecimalField(decimal_places=2, max_digits=5, default = 9.50)
    total           = models.DecimalField(decimal_places=3, max_digits=12, default = 0.000)
    status          = models.CharField(max_length = 12, choices = STATUS_LIST)
    creation_time   = models.DateTimeField(auto_now_add=True, editable= False)
    products        = models.TextField(editable=False, blank=True, null=True)

    objects = InvoiceManager()

    def __str__(self):
        return self.invoice_id




def invoice_pre_seve_reciever(instance, sender, *args, **kwargs):
    instance.total = float(instance.cart.total) + float(instance.shipping)
    product_list = [str(x.name)+' - '  for x in instance.cart.products.all()]
    instance.products = product_list
    if not instance.cart.user == None:
        instance.buyer = instance.cart.user.username
    else:
        instance.buyer ='Guest'
    if not instance.invoice_id:
        a = uuid.uuid4()
        t = datetime.now()
        id = str(a) + str(t)
        instance.invoice_id = id


pre_save.connect(invoice_pre_seve_reciever, sender=Invoice)
