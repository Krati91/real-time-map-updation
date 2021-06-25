import json
from asgiref.sync import sync_to_async

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Order
from .utils import create_map, create_vendor_map


class OrderConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        # print('connected', event)
        order_id = self.scope['url_route']['kwargs']['order_id']

        self.order = await self.get_order(order_id)
        self.group_name = f'Order_{order_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        # print('receive', event['text'])
        front_text = event.get('text', None)
        # print(front_text)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)

            runner_location = loaded_dict_data.get('location')
            await self.update_runner_location(runner_location)
            buyer_location = await self.get_buyer_location()
            vendor_location = await self.get_vendor_location()

            buyer_runner_map = create_map(buyer_location, runner_location)
            vendor_map = create_vendor_map(
                vendor_location, buyer_location, runner_location)

            context = {
                'map': json.dumps(buyer_runner_map),
                'vendor_map': json.dumps(vendor_map)
            }

            # print(context)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'map_message',
                    'text': json.dumps(context)
                }
            )

    async def map_message(self, event):
        # print('message', event)
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    async def websocket_disconnect(self, event):
        print('disconnected', event)
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    @database_sync_to_async
    def get_order(self, order_id):
        return Order.objects.get(pk=order_id)

    @database_sync_to_async
    def get_buyer_location(self):
        return self.order.get_buyer_city()

    @database_sync_to_async
    def get_vendor_location(self):
        return self.order.get_vendor_city()

    @database_sync_to_async
    def update_runner_location(self, location):
        self.order.orderstatus_set.get(status=2).holder.address_set.filter(
            is_primary=True).update(city=location)
