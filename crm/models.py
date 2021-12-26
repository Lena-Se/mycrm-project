"""
This module contains model classes for crm application
"""
from ckeditor.fields import RichTextField
from django.core.validators import RegexValidator
from django.db import models
from .customslug import slugify
from django.urls import reverse, reverse_lazy


class Phone(models.Model):
    """
         Model representing a phone number data for client company.
    """

    # validation function for phone number
    phone_validator = RegexValidator(regex=r'^(\+)?((\d{2,3}) ?\d|\d)(([ -]?\d)|( ?(\d{2,3}) ?)){5,12}\d$',
                                     message='Номер телефона в формате: "+380123456789".')

    # Phone number field
    number = models.CharField(max_length=13, verbose_name='телефон', validators=[phone_validator],
                              help_text='Номер телефона в формате: "+380123456789"')

    # Foreign key for Client object containing this Phone
    client = models.ForeignKey('Client', on_delete=models.CASCADE, null=True, verbose_name='компания')

    # Date and time of Phone object creation
    created = models.DateTimeField(auto_now_add=True)

    # Date and time of Phone object last update
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('client', '-created', '-updated')
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'

    def __str__(self):
        """
        Function for string representing of Phone object
        Args:
            self: Phone object
        Returns:
            (str) string value for Prone object displaying
        """
        return self.number


class Email(models.Model):
    """
         Model representing a email address data for client company.
    """

    # Email address field
    email_address = models.EmailField(verbose_name='email')

    # Foreign key for Client object containing this Email
    client = models.ForeignKey('Client', on_delete=models.CASCADE, null=True, verbose_name='компания')

    # Date and time of Email object creation
    created = models.DateTimeField(auto_now_add=True)

    # Date and time of Email object last update
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('client', 'email_address', '-created', '-updated')
        verbose_name = 'Email'
        verbose_name_plural = 'Email адреса'

    def __str__(self):
        """
        Function for string representing of Email object
        Args:
           self: Email object
        Returns:
          (str) string value for Email object displaying
        """
        return self.email_address


class Client(models.Model):
    """
         Model representing a client company data.
    """
    # Client's company name
    company_name = models.CharField(max_length=500, verbose_name='компания', db_index=True)

    # Client's contact person or director first and last names
    contact_person = models.CharField(max_length=300, verbose_name='контактное лицо (ФИО)',
                                      help_text='ФИО контактного лица / руководителя')

    # Information about client
    description = RichTextField(blank=True, verbose_name='описание')

    # Date and time of Client object creation
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан', db_index=True)

    # Date and time of Client object last update
    updated = models.DateTimeField(auto_now=True, verbose_name='изменен', db_index=True)

    # Address data of client
    address = models.CharField(max_length=500, blank=True, verbose_name='адрес')

    # Client slug - short string identifier
    slug = models.SlugField(max_length=250, unique=True, db_index=True)

    class Meta:
        ordering = ('company_name', 'created', 'updated')
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def get_absolute_url(self):
        """
        Returns url for Client model single object
        """
        return reverse('client-details', args=[self.slug])

    def save(self, *args, **kwargs):
        """
        Overrides standart model save function. Add custom non-cyrillic slug value for new Client object
        """
        if not self.slug:
            new_slug = slugify(self.company_name)
            if Client.objects.filter(slug=new_slug).count() > 0:
                new_slug += '_' + slugify(str(self.contact_person[:5]))
            self.slug = new_slug
        super(Client, self).save(*args, **kwargs)

    def __str__(self):
        """
        Function for string representing of Client object
        Args:
           self: CLient object
        Returns:
           (str) string value for Client object displaying
        """
        return self.company_name


class Project(models.Model):
    """
         Model representing a project data.
    """

    # Project name (title)
    name = models.CharField(max_length=500, verbose_name='Название проекта', db_index=True)

    # Project description
    description = RichTextField(blank=True, verbose_name='описание')

    # Date of project start
    start_date = models.DateField(verbose_name='дата начала', db_index=True)

    # Date of project end (may be blunk)
    end_date = models.DateField(blank=True, verbose_name='дата окончания', null=True, db_index=True)

    # Project price
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)

    # Company for which project belong
    company = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, verbose_name='компания', db_index=True)

    # Date and time of Project object creation
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан')

    # Date and time of Project object last update
    updated = models.DateTimeField(auto_now=True, verbose_name='изменен')

    class Meta:
        ordering = ('company', 'name', 'created')
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def get_absolute_url(self):
        """
        Returns url for Project model single object
        """
        return reverse('project-details', args=[str(self.pk)])

    def __str__(self):
        """
        Function for string representing of Project object
        Args:
           self: Project object
        Returns:
           (str) string value for Project object displaying
        """
        return self.name


