import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
  
  async def connect(self):
    self.room_name = self.scope['url_route']['kwargs']['room_name']
    self.room_group_name = f'chat_{self.room_name}'

    # Unir al grupo de WebSocket específico de la sala
    await self.channel_layer.group_add(
        self.room_group_name,
        self.channel_name
    )
    await self.accept()

  async def disconnect(self, close_code):
    # Salir del grupo de WebSocket específico de la sala
    await self.channel_layer.group_discard(
        self.room_group_name,
        self.channel_name
    )

  #recibir mensaje del WebSocket
  async def receive(self, text_data):
    data = json.loads(text_data)
    message = data['message']
    username = data['username']

    # Enviar mensaje al grupo
    await self.channel_layer.group_send(
        self.room_group_name,
        {
            'type': 'chat_message',
            'message': message,
            'username': username
        }
    )

  #Manejar el mensaje recibido
  async def chat_message(self, event):
    message = event['message']
    username = event['username']

    #Enviar el mensaje a WebSocket
    await self.send(text_data=json.dumps({
        'message': message,
        'username': username
    }))
  
        
class EchoConsumer(AsyncWebsocketConsumer):
  
  async def connect(self):
    #Acepta la conexión
    await self.accept()

    #Enviar estado de la conexión al usuario
    await self.send(text_data=json.dumps({
      'message': 'You are connected to the Echo Room!',
      'status': 'connected'
    }))

  async def disconnect(self, close_code):
    #Enviar estado de desconexión
    await self.send(text_data=json.dumps({
      'message': 'You have been disconnected!',
      'status': 'disconnected'
    }))

  async def receive(self, text_data):
    #Recibe el mensaje del usuario
    text_data_json = json.loads(text_data)
    message = text_data_json['message']

    #Enviar el mismo mensaje de vuelta (echo)
    await self.send(text_data=json.dumps({
        'message': f"{message}"
    }))


class GroupGuestConsumer(AsyncWebsocketConsumer):
  
  async def connect(self):
    # El nombre de la sala se pasa por la URL
    #self.room_name = self.scope['url_route']['kwargs']['room_name']
    self.room_name = 'guestroom'
    self.room_group_name = f'chat_{self.room_name}'

    # Unirse al grupo de la sala
    await self.channel_layer.group_add(
        self.room_group_name,
        self.channel_name
    )
    await self.accept()

  async def disconnect(self, close_code):
    # Salir del grupo de la sala cuando se desconecta
    await self.channel_layer.group_discard(
        self.room_group_name,
        self.channel_name
    )

  async def receive(self, text_data):
    data = json.loads(text_data)
    message = data['message']
    username = data.get('username', 'guest')
    # Enviar el mensaje al grupo de la sala
    await self.channel_layer.group_send(
        self.room_group_name,
        {
            'type': 'chat_message',  # Tipo de evento
            'message': message,
            'username': username
        }
    )

  async def chat_message(self, event):
    message = event['message']
    username = event['username']
    # Enviar el mensaje a todos los WebSockets conectados
    await self.send(text_data=json.dumps({
        'username': username,
        'message': message
    }))
  
  

