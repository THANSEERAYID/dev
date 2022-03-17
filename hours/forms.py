from dataclasses import field
from django.forms import ModelForm
from.models import Room
from.models import User
from django.contrib.auth.forms import UserCreationForm



class MyUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['name','avatar', 'username', 'email', 'password1', 'password2']
        

class RoomFrom(ModelForm):
    class Meta:
        model=Room
        fields= "__all__"
        exclude=['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model =User
        fields=['avatar', 'first_name', 'last_name', 'username', 'email' , 'password', 'bio']
