from django.urls import path
from .consumers import SubscriptionConsumer, TypingConsumer

websocket_urlpatterns = [
    path('graphql/', SubscriptionConsumer.as_asgi()),
    path('graphql/typing/', TypingConsumer.as_asgi()),
]