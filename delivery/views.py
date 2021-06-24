from users.models import CustomUser
from delivery.utils import get_coords
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Order, OrderStatus
from .utils import create_runner_map, get_coords, create_map, create_vendor_map


@login_required(login_url='../../admin')
def buyer_order_track(request, order_id):
    order = Order.objects.get(pk=order_id)
    order_current_status = OrderStatus.objects.get_order_current_status(order)

    buyer_location = order.get_buyer_city()
    vendor_location = order.get_vendor_city()
    current_location = ''
    icon = ''
    color = ''
    if order_current_status:
        current_location = order_current_status['holder'].address_set.get(
            is_primary=True).city
        color = 'orange'
        if order_current_status['status'] == 'Out for delivery':
            icon = 'stop'
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

    if status_obj.exists() and status_obj[0].get_status_display() == 'Out for delivery':
        buyer_location = status_obj[0].order.get_buyer_city()
        print(buyer_location)
        current_location = status_obj[0].holder.address_set.get(
            is_primary=True).city
        color = 'orange'
        icon = 'stop'

        m = create_map(buyer_location, current_location, color, icon)

        context = {
            'order': status_obj[0].order,
            'map': m
        }
    else:
        location = CustomUser.objects.get(user__username=request.user).address_set.get(
            is_primary=True).city
        m = create_runner_map(location)

        context = {
            'map': m
        }

    return render(request, 'delivery/runner.html', context)


@login_required(login_url='../../admin')
def vendor_order_track(request, order_id):
    order = Order.objects.get(pk=order_id)
    order_current_status = OrderStatus.objects.get_order_current_status(order)

    buyer_location = order.get_buyer_city()
    vendor_location = order.get_vendor_city()
    current_location = ''
    icon = ''
    color = ''
    if order_current_status:
        current_location = order_current_status['holder'].address_set.get(
            is_primary=True).city
        color = 'orange'
        if order_current_status['status'] == 'Out for delivery':
            icon = 'stop'
    else:
        current_location = vendor_location
        icon = 'shopping-cart'
        color = 'green'

    m = create_vendor_map(vendor_location, buyer_location,
                          current_location, color, icon)

    context = {
        'order': order,
        'map': m
    }

    return render(request, 'delivery/vendor.html', context)
