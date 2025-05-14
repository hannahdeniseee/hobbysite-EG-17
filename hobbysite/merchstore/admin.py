"""
This is the admin file to specify how the django admin is laid out with the
Merchstore app's models.
"""

from django.contrib import admin
from .models import Product, ProductType


class ProductAdmin(admin.ModelAdmin):
    """
    Specifies the search fields, filters, and fields
    for the product admin.
    """
    model = Product
    search_fields = ('name',)
    list_display = ('name', 'owner', 'product_type', 'price')
    list_filter = ('product_type',)


class ProductTypeAdmin(admin.ModelAdmin):
    """
    Specifies the search fields, filters, and fields
    for the product type admin.
    """
    model = ProductType
    search_fields = ('name',)
    list_display = ('name', 'description')
    list_filter = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
