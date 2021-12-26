"""
In this module there are constant data for interactions application
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class InteractionChoices(models.TextChoices):
    """
    In this class there are choices data for Interaction model reference_channel field
    """
    ONREQUEST = 'request', _('Заявка')
    MAIL = 'mail', _('Письмо')
    SITE = 'site', _('Сайт')
    CALL = 'call', _('Звонок')
    INITIATIVE = 'initiative', _('Инициатива компании')

