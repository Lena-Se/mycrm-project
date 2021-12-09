from ckeditor.fields import RichTextField
from django.db import models

# Create your models here.
from django.urls import reverse


class Phone(models.Model):
    number = models.CharField(max_length=13, verbose_name='телефон')
    client = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True, verbose_name='компания')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.number


class Email(models.Model):
    email_address = models.EmailField(verbose_name='email')
    client = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True, verbose_name='компания')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email_address


class Client(models.Model):
    company_name = models.CharField(max_length=500, verbose_name='компания')
    contact_person = models.CharField(max_length=300, verbose_name='контактное лицо (ФИО)')
    description = RichTextField(blank=True, verbose_name='описание')
    # models.TextField(blank=True, verbose_name='описание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='изменен')
    address = models.CharField(max_length=500, blank=True, verbose_name='адрес')
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        ordering = ('company_name', 'created', 'updated')
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def get_url(self):
        print(self.slug)
        print(reverse('client_detail', args=[self.slug]))
        return reverse('client_detail', args=[self.slug])
        #return reverse('client-detail', args=[str(self.id)])

    def __str__(self):
        return self.company_name


