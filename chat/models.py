from django.db import models
from django.utils import timezone

class User(models.Model):
  
  USERTYPE = [
    ('registered', 'Registered'),
    ('guest', 'Guest'),
  ]
  
  name = models.CharField(max_length=256, unique=True)
  privatekey = models.CharField(max_length=256, null=True, blank=True)
  usertype = models.CharField(max_length=32, choices=USERTYPE, default='guest')
  lastseen = models.DateTimeField(default=timezone.now, null=True, blank=True)
  datejoined = models.DateTimeField(default=timezone.now, null=True, blank=True)  # Date the user registered
  lastlogin = models.DateTimeField(null=True, blank=True)  # Last time the user logged in
  isactive = models.BooleanField(default=False)  # Active status
  ipaddress = models.GenericIPAddressField(null=True, blank=True)
  guesttoken = models.CharField(max_length=512, null=True, blank=True) #Token for guest identification
  useragent = models.CharField(max_length=512, null=True, blank=True)  #Browser/device info

  def __str__(self):
    return self.name
  
  def is_guest(self):
    return self.usertype == 'guest'
  
  def is_registered(self):
    return self.usertype == 'registered'
  
  def is_active(self):
    return self.isactive
  


class ChatRoom(models.Model):
  
  STATUS = [
    ('active', 'Active'),
    ('maintenance', 'In Maintenance'),
    ('closed', 'Closed'),
  ]
  
  name = models.CharField(max_length=255, unique=True)
  description = models.TextField(null=True, blank=True)
  createdat = models.DateTimeField(default=timezone.now)
  updatedat = models.DateTimeField(auto_now=True, null=True, blank=True)  # Actualizado cada vez que la sala cambia
  status = models.CharField(max_length=32, choices=STATUS, default='active')
  createdby = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_rooms')
  participants = models.ManyToManyField(User, blank=True, related_name='joined_rooms')
  maxparticipants = models.IntegerField(null=True, blank=True)
  onlineparticipants = models.ManyToManyField(User, blank=True, related_name='online_participants')
  totalmessages = models.IntegerField(default=0)
  private = models.BooleanField(default=False)
  
  def __str__(self):
    return self.name
  


class Message(models.Model):
  room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  content = models.TextField()
  timestamp = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return f'{self.user.name}: {self.content[:50]}'


