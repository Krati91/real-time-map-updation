from django.urls import path

from . import views

urlpatterns = [
    path('track-order/<int:order_id>',
         views.buyer_order_track, name='track-order'),
    path('runner-status/<int:user_id>',
         views.runner_status, name='runner-status'),
    path('vendor-track-order/<int:order_id>',
         views.vendor_order_track, name='vendor-track-order')
]
