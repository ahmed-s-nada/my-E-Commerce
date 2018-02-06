from django.contrib import admin
from .models import Invoice

# Register your models here.
class InvoiceAdmin(admin.ModelAdmin):
    fields         = ['invoice_id', 'cart', 'shipping', 'total', 'status', 'creation_time', 'buyer', 'products']
    list_display   = ['invoice_id', 'buyer', 'shipping', 'total', 'status', 'creation_time']
    list_filter    = ['invoice_id', 'cart', 'shipping', 'total', 'status', 'creation_time']

    readonly_fields = ['creation_time', 'invoice_id', 'products']
    # prepopulated_fields = {'total': ('cart.total',)}

    class Meta:
        model = Invoice

admin.site.register(Invoice, InvoiceAdmin)
