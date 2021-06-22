from django.contrib import admin

from .models import *
# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'product', 'placed_at']

    def product(self, obj):
        product = obj.products.count()

admin.site.register(Product)
admin.site.register(OrderStatus)
