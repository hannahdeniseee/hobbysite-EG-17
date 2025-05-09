from django import forms
from .models import Product, Transaction


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product 
        fields = ['name', 'owner', 'description', 'price', 'product_type',
                  'status', 'stock']
        widgets = {
            'status': forms.Select(choices=[
                ('Available', 'Available'),
                ('On sale', 'On sale'),
                ('Out of stock', 'Out of stock')
            ]),
            'product_type': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)
        super().__init__(*args, **kwargs)

        if user_profile:
            self.fields['owner'].initial = user_profile
        self.fields['owner'].disabled = True  # Prevent editing


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']
