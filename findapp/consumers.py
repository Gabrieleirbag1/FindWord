from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from .models import GameModel

class ChatConsumer(AsyncWebsocketConsumer):
    rooms = {}
    user_connections = {}
    ready_states = {}
    socket_connections = []
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user_id = self.scope['user'].id

        if self.room_name not in ChatConsumer.rooms:
            ChatConsumer.rooms[self.room_name] = 0
            ChatConsumer.user_connections[self.room_name] = set()
            ChatConsumer.ready_states[self.room_name] = {}

        ChatConsumer.rooms[self.room_name] += 1
        
        print(f"User {self.user_id} attempting to connect to room {self.room_name}")
        print(f"Current connections in room {self.room_name}: {ChatConsumer.user_connections[self.room_name]}")
        
        if self.user_id in ChatConsumer.user_connections[self.room_name]:
            await self.accept()  # Accept the connection first
            await self.close(code=4001)  # Then close with a custom code
        else:
            ChatConsumer.user_connections[self.room_name].add(self.user_id)
            
            if ChatConsumer.rooms[self.room_name] > 2:
                await self.accept()  # Accept the connection first
                await self.close(code=4000)  # Then close with the custom code
            else:
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )
                await self.accept()
                self.socket_connections.append(self)
                print(self.scope['user'].username, "connected to room", self.room_name)
                await self.set_ready_states(self.scope['user'].username)

    async def disconnect(self, close_code):
        try:
            self.socket_connections.remove(self)
        except ValueError:
            print("User not in socket connections")
            
        if self.room_name in ChatConsumer.rooms:
            ChatConsumer.rooms[self.room_name] -= 1
            if ChatConsumer.rooms[self.room_name] <= 0:
                del ChatConsumer.rooms[self.room_name]
                del ChatConsumer.user_connections[self.room_name]
                del ChatConsumer.ready_states[self.room_name]
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        try:
            print(f"User {self.user_id} disconnected from room {self.room_name}")
            print(f"Current connections in room {self.room_name}: {ChatConsumer.user_connections[self.room_name]}")
        except KeyError:
            print(f"Room {self.room_name} has no more connections")

        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(f"User {self.user_id} sent message: {text_data_json}")
        message = text_data_json['message']
        if message == "disconnect":
            ChatConsumer.user_connections[self.room_name].discard(self.user_id)
            await self.close()
            return
        
        if message == "ready_state":
            state = await self.str_bool_convert(text_data_json['state'])
            user = text_data_json['user']
            ChatConsumer.ready_states[self.room_name][self.user_id] = state
            await self.set_new_ready_state(user, state)

            if len(ChatConsumer.ready_states[self.room_name]) == 2:
                if all(ChatConsumer.ready_states[self.room_name].values()):
                    await self.reset_ready_states()
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'message': "start"
                        }
                    )
            return

        if message == "connect":
            user = text_data_json['user']
            print('new user:', user, 'in room', self.room_name)
            await self.send_to_all({
                'message': "username",
                'user': user
            })
            return
        
        if message == "rate":
            note = text_data_json['note']
            user = text_data_json['user']            
            await self.rate(user, note)
            return   

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

    async def str_bool_convert(self, text_data):
        if text_data == "ready":
            return True
        return False

    async def send_to_all(self, message):
        for connection in self.socket_connections:
            await connection.send(text_data=json.dumps(message))

    async def reset_ready_states(self):
        game = await sync_to_async(GameModel.objects.filter(room_name=self.room_name).first)()
        if game:
            game.player1_ready = False
            game.player2_ready = False
            await sync_to_async(game.save)()

    async def set_ready_states(self, username):
        game = await sync_to_async(GameModel.objects.filter(room_name=self.room_name).first)()
        if game:
            if username == game.player1:
                state = game.player1_ready
            elif username == game.player2:
                state = game.player2_ready
            ChatConsumer.ready_states[self.room_name][self.user_id] = state

    async def set_new_ready_state(self, user, state):      
        game = await sync_to_async(GameModel.objects.filter(room_name=self.room_name).first)()
        if game:
            if user == game.player1:
                game.player1_ready = state
            elif user == game.player2:
                game.player2_ready = state
            await sync_to_async(game.save)()

    async def rate(self, user, note):
        print('rating', user, 'with', note)
        game = await sync_to_async(GameModel.objects.filter(room_name=self.room_name).first)()
        if game:
            if game.player1 == user:
                game.player1_note = int(note)
            elif game.player2 == user:
                game.player2_note = int(note)
            # Sauvegarder le jeu de manière synchrone
            await sync_to_async(game.save)()