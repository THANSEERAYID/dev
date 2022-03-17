from email import message
from http.client import HTTPResponse
from multiprocessing import context
from pydoc_data.topics import topics
from dataclasses import field
from platformdirs import user_cache_dir
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from sqlalchemy import null
from .models import Room,Topic,Messages,User
from .forms import RoomFrom, UserForm, MyUserCreationForm
from django import forms 
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
# Create your views here.


def loginpage(request):
    page='login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method =='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, "User dosen't exists ")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "The Username OR Password doesn't exists")

    context={'page':page}
    return render(request, "dev/login_register.html", context)


def logoutpage(request):
    logout(request)
    return redirect('home')

def registerpage(request):
    form=MyUserCreationForm()

    if request.method=='POST':
        form = MyUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()

            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured in registration')
            
    return render(request, 'dev/login_register.html',{'form':form} )

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)
    )
    topics=Topic.objects.all()[0:5]
    room_count =rooms.count()
    room_messages=Messages.objects.filter(Q(room__topic__name__icontains=q))

    return render(request, 'dev/home.html',{
        'rooms':rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages
    })
def room(request, pk):
    room=Room.objects.get(id=pk)
    room_messages=room.messages_set.all()
    participants=room.participants.all()

    if request.method =='POST':
        message=Messages.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context={'room':room , 'room_messages': room_messages, 'participants':participants}
    return render(request, 'dev/room.html' , context)



def userProfile(request, pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_messages=user.messages_set.all()
    topics=Topic.objects.all()
    
    context={'user':user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics}
    return render(request, 'dev/profile.html', context)


@login_required(login_url='login')
def deleteMessage(request, pk):
    message=Messages.objects.get(id=pk)

    if request.user != message.user:
        return HTTPResponse("you can't delete someone else's message")

    if request.method=="POST":
        message.delete()
        return redirect('home')

    return render(request, 'dev/delete.html', {'obj':message})

@login_required(login_url='login')
def createRoom(request):
    form=RoomFrom()
    topics=Topic.objects.all()
    if request.method =='POST':

        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')


    context={'form':form, 'topics':topics}
    return render(request, "dev/room_form.html", context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room=Room.objects.get(id=pk)
    form=RoomFrom(instance=room)
    topics=Topic.objects.all()

    if request.user != room.host:
        return HTTPResponse('you are not the Host')

    if request.method =="POST":

        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room.name=request.POST.get('name')
        room.topic=request.POST.get('topic')
        room.description=request.POST.get('description')
        room.save()
        return redirect('home')


    context={"form":form , 'topics':topics, 'room':room}
    return render(request, 'dev/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room=Room.objects.get(id=pk)

    if request.user != room.host:
        return HTTPResponse("you can't delete someone else's room")

    if request.method=="POST":
        room.delete()
        return redirect('home')

    return render(request, 'dev/delete.html', {'obj':room})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form=UserForm(instance=user)

    if request.method=='POST':
        form =UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            login(request, user)
            return redirect('user-profile', pk=user.id)

    return render(request, 'dev/update-user.html', {'form': form

    } )


def topicPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics= Topic.objects.filter(name__icontains=q)

    return render(request, 'dev/topics.html',  { 'topics':topics

    })


def activityPage(request):
    room_messages=Messages.objects.all()
    return render(request, 'dev/activity.html', {'room_messages':room_messages
    })