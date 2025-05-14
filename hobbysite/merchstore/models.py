"""
This is the models file to specify the fields, ordering, and related methods
for the different models used in the Merchstore app.
"""

from django.db import models
from django.urls import reverse
from user_management.models import Profile


class ProductType(models.Model):
    """
    Represents a product type in Merchandise Store.

    Includes fields for name.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Represents a product in Merchandise Store.

    Includes fields for name, description, price,
    stock, status, product type, and owner.
    """
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('On Sale', 'On Sale'),
        ('Out of Stock', 'Out of Stock'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Available'
    )
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )
    owner = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='products',
        null=False
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('merchstore:merch-detail', args=[str(self.id)])


class Transaction(models.Model):
    """
    Represents a transaction in Merchandise Store.

    Includes fields for status, buyer, product, amount,
    and created_on.
    """
    STATUS_CHOICES = [
        ('On Cart', 'On Cart'),
        ('To Pay', 'To Pay'),
        ('To Ship', 'To Ship'),
        ('To Receive', 'To Receive'),
        ('Delivered', 'Delivered'),
    ]

    buyer = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        related_name='transactions_bought'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        related_name='transactions'
    )
    amount = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='On Cart'
    )
    created_on = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.product.price * self.amount

    def __str__(self):
        return f"{self.buyer} - {self.product} ({self.amount})"
