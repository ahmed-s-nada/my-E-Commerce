from django.contrib import admin
from .models import Product, ProductImages, ProductCategory, ProductsTag

# Register your models here.


class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 1
    max_num = 5

class ProductAdmin(admin.ModelAdmin):

    fields = [
        'name',
        'slug',
        'Manufacturer',
        'category',
        'tag',
        'discription',
        'cost',
        'price',
        'main_image',
        'featured',
        'Active',

    ]
    readonly_fields = ['slug', 'category',]

    inlines = [ ProductImagesInline, ]
    list_display = ('name','price' ,'category', 'tag')
    class Meta:
        model = Product


admin.site.register(ProductCategory)
admin.site.register(ProductsTag)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImages)
