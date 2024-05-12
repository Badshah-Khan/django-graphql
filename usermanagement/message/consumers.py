from channels.generic.websocket import AsyncWebsocketConsumer
import json

class SubscriptionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Parse incoming JSON data
        data = json.loads(text_data)

        # Extract the GraphQL subscription query from the data
        query = data.get('query')

        # Execute the GraphQL subscription query
        # (Implementation depends on your setup)

    async def send_update(self, data):
        await self.send(text_data=json.dumps(data))