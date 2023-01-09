import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import translation


class CashierConsumer(WebsocketConsumer):
    GROUP_NAME = "cashier_q_channel_group"

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(self.GROUP_NAME, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.GROUP_NAME, self.channel_name)

    def receive(self, text_data):
        data = json.loads(text_data)

    def cashier_message(self, data):
        cashier_number = data.get("num_cashier", 0)
        language = data.get("language", settings.LANGUAGE_CODE)
        context = {'cashier_number': int(cashier_number)}
        translation.activate(language)
        message_html = render_to_string("cashier_message.html", context)
        self.send(text_data=message_html)
