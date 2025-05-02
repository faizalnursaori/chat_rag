import json

from channels.generic.websocket import AsyncWebsocketConsumer

from chats.tasks import process_chat


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("notification", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notification", self.channel_name)

    async def send_notification(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.document_id = self.scope["url_route"]["kwargs"]["document_id"]
        self.group_name = f"chat_{self.document_id}"

        await self.accept()
        await self.channel_layer.group_add("chat", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("chat", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        # print(f"Received message: {message}")
        process_chat(message, self.document_id)

    async def send_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
