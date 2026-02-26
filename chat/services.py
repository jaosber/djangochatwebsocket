from .models import Message, ChatRoom, User
from django.utils import timezone


#-------------- Rutinas - User

def create_guest_user(ipaddress, useragent):
  guest_name = generate_guest_name()
  guest_user = User.objects.create(
      name=guest_name,
      usertype='guest',
      ipaddress=ipaddress,
      useragent=useragent,
      datejoined=timezone.now(),
      lastseen=timezone.now(),
      isactive=True
  )
  return guest_user

def generate_guest_name():
  base_name = "guest"
  suffix = User.objects.count() + 1  #Simple logica para generar nombres unicos
  return f"{base_name}{suffix}"

def is_username_taken(name):
  return User.objects.filter(name=name).exists()
  

def create_registered_user(name, private_key, ipaddress=None, useragent=None):
    """
    Crea un nuevo usuario de tipo registrado.

    Args:
        name (str): Nombre del usuario (debe ser único).
        private_key (str): Clave privada asociada al usuario.
        ipaddress (str, opcional): Dirección IP del usuario.
        useragent (str, opcional): Información del navegador o dispositivo del usuario.

    Returns:
        User: El nuevo usuario registrado.
        None: Si el nombre de usuario ya está tomado.
    """
    if User.objects.filter(name=name).exists():
        print(f"Username '{name}' is already taken.")
        return None

    # Crear el nuevo usuario
    new_user = User.objects.create(
        name=name,
        privatekey=private_key,
        usertype='registered',  # Usuario registrado
        lastseen=timezone.now(),
        datejoined=timezone.now(),
        isactive=True,  # Marcamos el usuario como activo
        ipaddress=ipaddress,
        useragent=useragent
    )

    print(f"User '{new_user.name}' created successfully.")
    return new_user



#-------------- Rutinas - ChatRoom 


def get_chatroom_info(room_name):
  
  """
  Obtiene toda la información de una sala de chat específica.

  Args:
      room_name (str): El nombre de la sala de chat.

  Returns:
      dict: Un diccionario con toda la información de la sala de chat.
      None: Si la sala de chat no existe.
  """
  try:
    # Buscar la sala de chat por nombre
    room = ChatRoom.objects.get(name=room_name)
    
    # Obtener los participantes
    participants = room.participants.all()
    participant_list = [user.name for user in participants]
    
    # Obtener los participantes online
    online_participants = room.onlineparticipants.all()
    online_participant_list = [user.name for user in online_participants]
    
    # Contar los mensajes en la sala
    total_messages = room.messages.count()
    
    # Construir un diccionario con toda la información
    chatroom_info = {
        'name': room.name,
        'description': room.description,
        'status': room.status,
        'created_by': room.createdby.name if room.createdby else 'No creator',
        'created_at': room.createdat,
        'updated_at': room.updatedat,
        'participants': participant_list,
        'online_participants': online_participant_list,
        'total_messages': total_messages,
        'max_participants': room.maxparticipants,
        'private': room.private,
    }

    return chatroom_info
    
  except ChatRoom.DoesNotExist:
    print(f"Room '{room_name}' does not exist.")
    return None




#Rutinas - Message

def create_message(room_name, username, content):
  """
  Crea un nuevo mensaje en la sala de chat específica.

  Args:
      room_name (str): Nombre de la sala de chat.
      username (str): Nombre de usuario que envía el mensaje.
      content (str): Contenido del mensaje.

  Returns:
      Message: El mensaje recién creado o None si el usuario o la sala no existen.
  """
  try:
    room = ChatRoom.objects.get(name=room_name)
    user = User.objects.get(name=username)
    
    # Crear el mensaje
    new_message = Message.objects.create(
        room=room,
        user=user,
        content=content,
        timestamp=timezone.now()
    )
    return new_message
    
  except ChatRoom.DoesNotExist:
      print(f"Room '{room_name}' does not exist.")
      return None
  except User.DoesNotExist:
    print(f"User '{username}' does not exist.")
    return None


def get_all_messages_from_room(room_name):
  """
  Obtiene todos los mensajes de una sala de chat específica.

  Args:
      room_name (str): Nombre de la sala de chat.

  Returns:
      QuerySet: Un queryset con todos los mensajes de la sala o None si la sala no existe.
  """
  try:
    
    room = ChatRoom.objects.get(name=room_name)
    messages = Message.objects.filter(room=room).order_by('timestamp')
    
    # Si deseas retornar un diccionario o lista con todos los campos, puedes recorrer el queryset
    message_list = [
        {
            'user': message.user.name,
            'content': message.content,
            'timestamp': message.timestamp
        } for message in messages
    ]
    
    return message_list
    
  except ChatRoom.DoesNotExist:
    print(f"Room '{room_name}' does not exist.")
    return None



