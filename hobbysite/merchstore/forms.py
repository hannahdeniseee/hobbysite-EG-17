from django import forms
from .models import Product, Transaction


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product 
        fields = ['name', 'description', 'price', 'product_type',
                  'status', 'stock']
        widgets = {
            'status': forms.Select(choices=[
                ('Available', 'Available'),
                ('On sale', 'On sale'),
                ('Out of stock', 'Out of stock')
            ]),
            'product_type': forms.Select(),
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']
