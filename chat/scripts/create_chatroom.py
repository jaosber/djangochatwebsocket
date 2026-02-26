from chat.models import ChatRoom, User

def create_welcome_room():
  # Buscar el usuario 'Admin' como creador de la sala
  creator = User.objects.filter(name='admin').first()

  if not creator:
    print("Admin user not found. Please create an Admin user first.")
    return

  # Verificar si la sala 'Welcome' ya existe
  if ChatRoom.objects.filter(name="welcome").exists():
    print("Chat room 'welcome' already exists.")
    return

  # Crear la sala de chat 'Welcome'
  welcome_room = ChatRoom.objects.create(
    name="welcome",
    description="Public welcome room for everyone",
    status="active",
    createdby=creator,  # o None si no hay un creador
    private=False  # La sala es pública
  )

  print(f"Chat room '{welcome_room.name}' created successfully.")