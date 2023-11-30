from django.contrib import admin

# Register your models here.
from .models import Games, Players

admin.site.register(Games)
admin.site.register(Players)