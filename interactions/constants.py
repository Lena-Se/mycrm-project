from django.db import models
from django.utils.translation import gettext_lazy as _

# INTERACTION_CHOICES = [
#     ('request', 'Заявка'),
#     ('mail', 'Письмо'),
#     ('site', 'Сайт'),
#     ('call', 'Звонок'),
#     ('initiative', 'Инициатива компании')
# ]


class InteractionChoices(models.TextChoices):
    ONREQUEST = 'request', _('Заявка')
    MAIL = 'mail', _('Письмо')
    SITE = 'site', _('Сайт')
    CALL = 'call', _('Звонок')
    INITIATIVE = 'initiative', _('Инициатива компании')

