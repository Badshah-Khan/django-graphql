import os
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import message.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'usermanagement.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(URLRouter(
        message.routing.websocket_urlpatterns
    )),
})