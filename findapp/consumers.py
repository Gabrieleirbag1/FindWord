from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    rooms = {}
    user_connections = {}

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user_id = self.scope['user'].id

        if self.room_name not in ChatConsumer.rooms:
            ChatConsumer.rooms[self.room_name] = 0
            ChatConsumer.user_connections[self.room_name] = set()
            
        ChatConsumer.rooms[self.room_name] += 1
        
        print(f"User {self.user_id} attempting to connect to room {self.room_name}")
        print(f"Current connections in room {self.room_name}: {ChatConsumer.user_connections[self.room_name]}")
        
        if self.user_id in ChatConsumer.user_connections[self.room_name]:
            await self.accept()  # Accept the connection first
            # await self.send(text_data=json.dumps({
            #     'message': 'You are already connected to this room.'
            # }))
            await self.close(code=4001)  # Then close with a custom code
        else:
            ChatConsumer.user_connections[self.room_name].add(self.user_id)
            
            if ChatConsumer.rooms[self.room_name] > 2:
                await self.accept()  # Accept the connection first
                # await self.send(text_data=json.dumps({
                #     'message': 'Room is full. Redirecting to lobby...'
                # }))
                await self.close(code=4000)  # Then close with the custom code
            else:
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )
                await self.accept()

    async def disconnect(self, close_code):
        if self.room_name in ChatConsumer.rooms:
            ChatConsumer.rooms[self.room_name] -= 1
            if ChatConsumer.rooms[self.room_name] <= 0:
                del ChatConsumer.rooms[self.room_name]
                del ChatConsumer.user_connections[self.room_name]
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        print(f"User {self.user_id} disconnected from room {self.room_name}")
        print(f"Current connections in room {self.room_name}: {ChatConsumer.user_connections[self.room_name]}")
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))