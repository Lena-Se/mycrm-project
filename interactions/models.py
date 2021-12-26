from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse_lazy

from crm.models import Project
from .constants import InteractionChoices


class Keyword(models.Model):
    """
      Model representing a keywords for interaction filtering.
    """
    word_validator = RegexValidator(regex=r'\w+$', message='Ключевое слово для поиска взаимодействий.')
    word = models.CharField(max_length=300, unique=True, help_text="Добавьте ключевое слово для взаимодействия",
                            verbose_name='ключевое слово', blank=True, db_index=True, validators=[word_validator])

    class Meta:
        ordering = ('word',)
        verbose_name = 'Ключевое слово'
        verbose_name_plural = 'Ключевые слова'

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.word


class Interaction(models.Model):
    """
         Model representing an interaction data for project of client company.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='взаимодействие', db_index=True)
    reference_channel = models.CharField(max_length=25, choices=InteractionChoices.choices,
                                         verbose_name='канал обращения', db_index=True, default=InteractionChoices.MAIL)
    description = RichTextField(blank=True, verbose_name='описание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='изменен')
    manager = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, verbose_name='менеджер',
                                db_index=True)
    keyword = models.ManyToManyField(Keyword, help_text="Выберите ключевые слова для взаимодействия",
                                     verbose_name='Ключевые слова', db_index=True)
    rating = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='рейтинг', null=True, blank=True,
                                 editable=False, db_index=True)

    class Meta:
        ordering = ('project', '-created')
        verbose_name = 'Взаимодействие'
        verbose_name_plural = 'Взаимодействия'

    def get_absolute_url(self):
        return reverse_lazy('interaction-details', args=[self.pk])

    def __str__(self):
        return self.get_reference_channel_display() + " - " + self.project.name


class Mark(models.Model):
    """
         Model representing a mark for interaction of some project.
    """
    rate = models.IntegerField(default=0, verbose_name='оценка')
    interaction = models.ForeignKey(Interaction, on_delete=models.CASCADE, verbose_name='взаимодействие')
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='изменен')
    manager = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='менеджер')

    class Meta:
        ordering = ('interaction', 'rate', '-created')
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    def __str__(self):
        return str(self.rate)


