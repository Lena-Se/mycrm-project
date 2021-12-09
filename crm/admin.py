from django.contrib import admin
from .models import Client, Phone, Email
# Register your models here.

admin.site.register(Client)
admin.site.register(Phone)
admin.site.register(Email)
