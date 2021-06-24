from django.contrib import admin

from .models import *
# Register your models here.


class OrderStatusAdmin(admin.TabularInline):
    model = OrderStatus


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'product', 'placed_at']
    inlines = [OrderStatusAdmin]

    def product(self, obj):
        return obj.products.count()


admin.site.register(Product)
