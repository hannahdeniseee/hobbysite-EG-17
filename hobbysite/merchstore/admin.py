from django.contrib import admin
from .models import Product, ProductType


class ProductAdmin(admin.ModelAdmin):
    model = Product
    search_fields = ('name',)
    list_display = ('name', 'product_type', 'price')
    list_filter = ('product_type',)


class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType
    search_fields = ('name',)
    list_display = ('name', 'description')
    list_filter = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
