from django.contrib import admin
from .models import Client, Phone, Email, Project

# admin.site.register(Client)
admin.site.register(Phone)
admin.site.register(Email)
admin.site.register(Project)


class PhonesInline(admin.TabularInline):
    model = Phone
    extra = 2


class EmailsInline(admin.TabularInline):
    model = Email
    extra = 2


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_person', 'address')
    inlines = [PhonesInline, EmailsInline]
