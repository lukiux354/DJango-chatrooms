from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import ChatApp.routing

application = ProtocolTypeRouter({
    #"http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            ChatApp.routing.websocket_urlpatterns
        )
    ),
})