from django.contrib import admin

from hours.models import Room,Messages,Topic,User


# Register your models here.


admin.site.register(Room)
admin.site.register(Messages)
admin.site.register(Topic)
admin.site.register(User)