from ckeditor.fields import RichTextField
from django.core.validators import RegexValidator
from django.db import models
from .constants import INTERACTION_CHOICES

# Create your models here.
from django.urls import reverse, reverse_lazy


class Phone(models.Model):
    phone_validator = RegexValidator(regex=r'^(\+)?((\d{2,3}) ?\d|\d)(([ -]?\d)|( ?(\d{2,3}) ?)){5,12}\d$',
                                     message='Номер телефона в формате: "+380123456789".')
    number = models.CharField(max_length=13, verbose_name='телефон', validators=[phone_validator],
                              help_text='Номер телефона в формате: "+380123456789"')
    client = models.ForeignKey('Client', on_delete=models.CASCADE, null=True, verbose_name='компания')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('client', '-created', '-updated')
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'

    def __str__(self):
        return self.number


class Email(models.Model):
    email_address = models.EmailField(verbose_name='email')
    client = models.ForeignKey('Client', on_delete=models.CASCADE, null=True, verbose_name='компания')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('client', 'email_address', '-created', '-updated')
        verbose_name = 'Email'
        verbose_name_plural = 'Email адреса'

    def __str__(self):
        return self.email_address


class Client(models.Model):
    slug_validator = RegexValidator(regex=r'\w+$', message='Уникальное имя для представления клиента латиницей.')
    company_name = models.CharField(max_length=500, verbose_name='компания')
    contact_person = models.CharField(max_length=300, verbose_name='контактное лицо (ФИО)',
                                      help_text='ФИО контактного лица / руководителя')
    description = RichTextField(blank=True, verbose_name='описание')
    # models.TextField(blank=True, verbose_name='описание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='изменен')
    address = models.CharField(max_length=500, blank=True, verbose_name='адрес')
    slug = models.SlugField(max_length=250, unique=True, validators=[slug_validator], db_index=True)

    class Meta:
        ordering = ('company_name', 'created', 'updated')
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def get_absolute_url(self):
        return reverse('client-details', args=[self.slug])

    def __str__(self):
        return self.company_name


class Project(models.Model):
    name = models.CharField(max_length=500, verbose_name='Название проекта')
    description = RichTextField(blank=True, verbose_name='описание')
    start_date = models.DateField(verbose_name='дата начала')
    end_date = models.DateField(blank=True, verbose_name='дата окончания', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    company = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, verbose_name='компания')
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='изменен')

    class Meta:
        ordering = ('company', 'name', 'created')
        verbose_name = 'Проект'
        verbose_name_plural = 'Прокеты'

    def get_absolute_url(self):
        return reverse('project-details', args=[str(self.id)])

    def __str__(self):
        return self.name


class Interaction(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='взаимодействие')
    reference_channel = models.CharField(max_length=25, choices=INTERACTION_CHOICES)
    description = RichTextField(blank=True, verbose_name='описание')
    like = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='изменен')

    def get_absolute_url(self):
        return reverse('interaction_detail', args=[self.id])

    def __str__(self):
        return self.reference_channel + " - " + self.project.name
