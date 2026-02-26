from django.shortcuts import render


def home(request):
  return render(request, 'home.html') 


def room(request):
  return render(request, 'room.html') 


def chatroom(request):
  return render(request, 'chatroom.html')


def guestroom(request):
  return render(request, 'guestroom.html')


def echoroom(request):
  return render(request, 'echoroom.html') 
