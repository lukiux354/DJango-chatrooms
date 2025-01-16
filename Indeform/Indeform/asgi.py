import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import ChatApp.routing  # Import ChatApp.routing directly
from channels.db import database_sync_to_async

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Indeform.settings')

application = ProtocolTypeRouter({
    # Uncomment if you also want to support HTTP requests
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            ChatApp.routing.websocket_urlpatterns  # Correctly reference ChatApp's routing
        )
    ),
})