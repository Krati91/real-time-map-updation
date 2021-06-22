from django.db import models

from users.models import CustomUser, Address
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=150)
    vendor = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, limit_choices_to={'type': 2}, null=True)

    def __str__(self):
        return f'{self.name} by {self.vendor.user.username}'


class Order(models.Model):
    buyer = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, limit_choices_to={'type': 1}, null=True)
    products = models.ManyToManyField(Product)
    placed_at = models.DateTimeField(auto_now_add=True)
    estimated_delivery_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'Order by {self.buyer.user.username} placed at {self.placed_at.date()}'

    def get_buyer_city(self):
        return self.buyer.address_set.get(is_primary=True).city

    def get_vendor_city(self):
        vendor = self.products.all()[0].vendor
        return vendor.address_set.get(is_primary=True).city


STATUS_CHOICES = [
    (2, 'Out for delivery'),
    (3, 'Delivered')
]


class OrderStatusManager(models.Manager):
    def get_order_current_status(self, order):
        order_status = [{'status': status.get_status(),
                         'last_update': status.updated_at,
                         'holder': status.holder
                         }
                        for status in OrderStatus.objects.filter(
            order=order).order_by('-updated_at')]

        return order_status[0] if len(order_status) else {}


class OrderStatus(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES)
    holder = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Order statuses'

    def __str__(self):
        return f'Order by {self.order.buyer.user.username} at {self.holder.address_set.get(is_primary=True).city}'

    def get_status(self):
        return self.get_status_display()

    objects = OrderStatusManager()
