from django.db import models

# Create your models here.
class Phone(models.Model):
    number = models.CharField(max_length=13)
    




class Client(models.Model):
    name = models.CharField(max_length=500)
    contact_person = models.CharField(max_length=300)

