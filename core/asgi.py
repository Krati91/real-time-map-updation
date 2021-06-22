import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from django.urls import path

from delivery.consumers import OrderConsumer


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = ProtocolTypeRouter({
    # WebSocket handler
    'websocket': AllowedHostsOriginValidator(AuthMiddlewareStack(
        URLRouter([
            path('order/<int:order_id>', OrderConsumer.as_asgi()),
        ])
    )
    )
})
