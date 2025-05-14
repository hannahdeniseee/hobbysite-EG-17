"""
This is the forms file to specify the different types of forms
used in the Forum app.
"""

from django import forms
from .models import Product, Transaction


class ProductForm(forms.ModelForm):
    """
    Form for creating products in the Merchandise Store.

    Includes all fields.
    """
    class Meta:
        model = Product
        fields = ['name', 'product_type', 'description', 'price', 
                  'status', 'stock']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'custom-name-field'}),
            'product_type': forms.Select(attrs={'class': 'custom-pt-field'}),
            'description': forms.Textarea(
                attrs={'class': 'custom-desc-field'}),
            'price': forms.NumberInput(attrs={'class': 'custom-price-field'}),
            'status': forms.Select(
                choices=[
                    ('Available', 'Available'),
                    ('On sale', 'On sale'),
                    ('Out of stock', 'Out of stock')
                ],
                attrs={'class': 'custom-status-field'}),
            'stock': forms.NumberInput(attrs={'class': 'custom-stock-field'}),
        }


class TransactionForm(forms.ModelForm):
    """
    Form for transactions in the Merchandise Store.

    Includes amount field only.
    """
    class Meta:
        model = Transaction
        fields = ['amount']

        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'custom-amount-field'}),   
        }
