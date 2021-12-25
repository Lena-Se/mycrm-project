from ckeditor.fields import RichTextField
from django.core.validators import RegexValidator
from django.db import models
from .customslug import slugify
from django.urls import reverse, reverse_lazy


class Phone(models.Model):
    """
         Model representing a phone number data for client company.
    """
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
    """
         Model representing a email address data for client company.
    """
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
    """
         Model representing a client company data.
    """
    # slug_validator = RegexValidator(regex=r'\w+$', message='Уникальное имя для представления клиента латиницей.')
    company_name = models.CharField(max_length=500, verbose_name='компания', db_index=True)
    contact_person = models.CharField(max_length=300, verbose_name='контактное лицо (ФИО)',
                                      help_text='ФИО контактного лица / руководителя')
    description = RichTextField(blank=True, verbose_name='описание')
    # models.TextField(blank=True, verbose_name='описание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан', db_index=True)
    updated = models.DateTimeField(auto_now=True, verbose_name='изменен', db_index=True)
    address = models.CharField(max_length=500, blank=True, verbose_name='адрес')
    slug = models.SlugField(max_length=250, unique=True, db_index=True)  # validators=[slug_validator]

    class Meta:
        ordering = ('company_name', 'created', 'updated')
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def get_absolute_url(self):
        return reverse('client-details', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            new_slug = slugify(self.company_name)
            if Client.objects.filter(slug=new_slug).count() > 0:
                new_slug += '_' + slugify(str(self.contact_person[:5]))
            self.slug = new_slug
        super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return self.company_name


class Project(models.Model):
    """
         Model representing a project data.
    """
    name = models.CharField(max_length=500, verbose_name='Название проекта', db_index=True)
    description = RichTextField(blank=True, verbose_name='описание')
    start_date = models.DateField(verbose_name='дата начала', db_index=True)
    end_date = models.DateField(blank=True, verbose_name='дата окончания', null=True, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    company = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, verbose_name='компания', db_index=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='изменен')

    class Meta:
        ordering = ('company', 'name', 'created')
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def get_absolute_url(self):
        return reverse('project-details', args=[str(self.pk)])

    def __str__(self):
        return self.name


