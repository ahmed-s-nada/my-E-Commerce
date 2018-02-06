from django.contrib import admin
from .models import Cart
# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'total')
    search_fields = ('id', 'user__username', 'total', 'products__name')
    class Meta:
        model = Cart
admin.site.register(Cart, CartAdmin)
