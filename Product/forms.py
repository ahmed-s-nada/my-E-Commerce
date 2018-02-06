from django import forms
from Product.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model  = Product
        fields = '__all__'
        # fields = ['Name','Category','Manufacturer']
        template_name = 'Product/product_form.html'
