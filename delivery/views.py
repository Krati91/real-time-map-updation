from users.models import CustomUser
from delivery.utils import get_coords
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Order, OrderStatus
from .utils import create_runner_map, get_coords, create_map


@login_required(login_url='../../admin')
def buyer_order_track(request, order_id):
    order = Order.objects.get(pk=order_id)
    order_current_status = OrderStatus.objects.get_order_current_status(order)

    buyer_location = order.get_buyer_city()
    vendor_location = order.get_vendor_city()
    current_location = ''
    icon = ''
    color = ''
    runner_id = 0
    if order_current_status:
        current_location = order_current_status['holder'].address_set.get(
            is_primary=True).city
        color = 'orange'
        if order_current_status['status'] == 'Out for delivery':
            icon = 'stop'
            runner_id = order_current_status['holder'].user.id
    else:
        current_location = vendor_location
        icon = 'shopping-cart'
        color = 'green'

    m = create_map(buyer_location, current_location, color, icon)

    context = {
        'order': order,
        'map': m
    }

    return render(request, 'delivery/track-order.html', context)


@login_required(login_url='../../admin')
def runner_status(request, user_id):
    status_obj = OrderStatus.objects.filter(
        holder__user__id=user_id)

    context = {}

    if status_obj.exists():
        context = {
            'order': status_obj[0].order,
        }
    else:
        location = CustomUser.objects.get(user__username=request.user).address_set.get(
            is_primary=True).city
        m = create_runner_map(location)

        context = {
            'map': m
        }

    return render(request, 'delivery/runner.html', context)
