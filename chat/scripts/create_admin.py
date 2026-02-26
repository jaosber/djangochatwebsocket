from chat.models import User
from django.utils import timezone

def create_admin_user():
  
  if not User.objects.filter(name="admin").exists():
    
    admin_user = User.objects.create(
        name="admin",
        privatekey="2cf24dba5fb0a30e26e83b2ac5b9e29e",
        usertype="registered",
        lastseen=timezone.now(),
        datejoined=timezone.now(),
        isactive=True,
        ipaddress="127.0.0.1",
        useragent="Admin browser",
    )
    print(f"Admin user '{admin_user.name}' created successfully.")
  else:
      print("Admin user already exists.")
      

#create_admin_user()
