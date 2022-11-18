from django.urls import path

from . import consumers

# websocket_urlpatterns = [
#   path('ws//', consumers.ChatConsumer.as_asgi()), # Using asgi
# ]

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path


# URLs that handle the WebSocket connection are placed here.
websocket_urlpatterns=[
                    re_path(
                        r"ws/1/$", consumers.ChatConsumer.as_asgi()
                    ),
                ]

application = ProtocolTypeRouter( 
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(
               websocket_urlpatterns
            )
        ),
    }
)

# from django.urls import path, re_path
# from . import consumers
# from . import views

# app_name = 'django_private_chat2'
# websocket_urlpatterns = [
#     re_path(r'^chat_ws$', consumers.ChatConsumer.as_asgi()),
# ]