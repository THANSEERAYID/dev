from django.urls import URLPattern, path
from .import views


urlpatterns=[
    path('login/',views.loginpage, name="login"),
    path('logout/',views.logoutpage, name="logout"),
    path('register/',views.registerpage, name="register"),

    path('',views.home ,name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('profile/<str:pk>', views.userProfile, name='user-profile'),

    path('createRoom/', views.createRoom, name="createRoom"),
    path('updateRoom/<str:pk>/', views.updateRoom, name="updateRoom"),
    path('deleteRoom/<str:pk>/', views.deleteRoom, name="deleteRoom"),
    path('deleteMessage/<str:pk>/', views.deleteMessage, name="delete-message"),
    path('updateuser/', views.updateUser, name="update-user"),

    ### mobile responsive urls
    path('topics/', views.topicPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
]