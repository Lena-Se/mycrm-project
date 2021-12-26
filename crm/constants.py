"""
In this module there are constant data for crm application
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class SortChoices(models.TextChoices):
    """
    Class contains choices data for Client list sorting
    """
    COMPANY = 'company_name', _('название')
    COMPANY_DSC = '-company_name', _('название (по убыванию)')
    CREATED = 'created', _('дата создания')
    CREATED_DSC = '-created', _('дата создания (по убыванию)')
    UPDATED = 'updated', _('дате изменения')
    UPDATED_DSC = '-updated', _('дате изменения (по убыванию)')

