from django.db import models
from django.utils.translation import gettext_lazy as _

# SORT_CHOICES = [
#     ["company_name", "названию"],
#     ["-company_name", "названию (по убыванию)"],
#     ["updated", "дате изменения"],
#     ["-updated", "дате изменения (по убыванию)"],
#     ["created", "дате создания"],
#     ["-created", "дате создания (по убыванию)"],
# ]


class SortChoices(models.TextChoices):
    COMPANY = 'company_name', _('название')
    COMPANY_DSC = '-company_name', _('название (по убыванию)')
    CREATED = 'created', _('дата создания')
    CREATED_DSC = '-created', _('дата создания (по убыванию)')
    UPDATED = 'updated', _('дате изменения')
    UPDATED_DSC = '-updated', _('дате изменения (по убыванию)')

