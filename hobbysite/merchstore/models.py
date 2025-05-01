from django.db import models
from django.urls import reverse
from django.conf import settings 


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model): 
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('On Sale', 'On Sale'),
        ('Out of Stock', 'Out of Stock'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_type = models.ForeignKey(
            ProductType, 
            on_delete=models.SET_NULL, 
            null=True,
            related_name='products')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # CHECK THIS LATER
        on_delete=models.CASCADE, 
        related_name='products')
    stock = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, 
                              choices=STATUS_CHOICES, default='Available')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('merchstore:merch-detail', args=[str(self.id)])


class Transaction(models.Model):
    STATUS_CHOICES = [
        ('On Cart', 'On Cart'),
        ('To Pay', 'To Pay'),
        ('To Ship', 'To Ship'),
        ('To Receive', 'To Receive'),
        ('Delivered', 'Delivered'),
    ]
    buyer = models.ForeignKey(
         settings.AUTH_USER_MODEL,
         on_delete=models.SET_NULL, 
         related_name='transactions_bought')

    product = models.ForeignKey(
         settings.AUTH_USER_MODEL,
         on_delete=models.SET_NULL, 
         related_name='transactions'
    )

    amount = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, 
                              choices=STATUS_CHOICES, default='On Cart')
    created_on = models.DateTimeField(auto_now_add=True)
