from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CrmUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'user_photo')
    model = User


admin.site.register(User, CrmUserAdmin)




