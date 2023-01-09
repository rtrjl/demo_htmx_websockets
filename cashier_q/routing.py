from django.urls import re_path

from cashier_q import consumers

websocket_urlpatterns = [
    re_path(r"^ws/cashier_q$", consumers.CashierConsumer.as_asgi()),
]