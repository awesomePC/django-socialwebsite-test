import json

from channels.generic.websocket import AsyncWebsocketConsumer # The class we're using
from asgiref.sync import sync_to_async # Implement later

class ChatConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    self.room_name = self.scope['url_route']['kwargs']['room_name']
    self.room_group_name = 'chat_%s' % self.room_name
    print("websocket")
    # Join room group
    await self.channel_layer.group_add(
      self.room_group_name,
      self.channel_name
    )

    await self.accept()

  async def disconnect(self, close_code):
    # Leave room group
    await self.channel_layer.group_discard(
      self.room_group_name,
      self.channel_name
  )

  # Receive message from WebSocket
  async def receive(self, text_data):
    data = json.loads(text_data)
    message = data['message']
    username = data['username']
    room = data['room']

    # Send message to room group
    await self.channel_layer.group_send(
        self.room_group_name,
        {
        'type': 'chat_message',
        'message': message,
        'username': username
        }
    )

# Receive message from room group
async def chat_message(self, event):
  message = event['message']
  username = event['username']

  # Send message to WebSocket
  await self.send(text_data=json.dumps({
    'message': message,
    'username': username
  }))