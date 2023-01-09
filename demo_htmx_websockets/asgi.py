"""
ASGI config for demo_htmx_websockets project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.asgi import get_asgi_application
import cashier_q.routing

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo_htmx_websockets.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(URLRouter(cashier_q.routing.websocket_urlpatterns))
        ,
    }
)
