from django.contrib import admin
from .models import Product, ProductType


class ProductAdmin(admin.ModelAdmin):
    model = Product
    search_fields = ('name',) 
    list_display = ('name',)  
    list_filter = ('name',)  


class ProductTypeAdmin(admin.ModelAdmin):
    model = ProductType
    search_fields = ('name',)
    list_display = ('name',)
    list_filter = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType, ProductAdmin)
