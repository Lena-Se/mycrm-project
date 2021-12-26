"""
This module contains form-classes for crm application

Attributes:
   PhoneInlineFormset: inlineformset for Phone objects in Client model
   EmainInlineFormset: inlineformset for Email objects in Client model
"""
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.forms import DateTimeField
from django.forms.models import inlineformset_factory, ModelForm
from .models import Client, Phone, Email, Project
from django.contrib.admin.widgets import AdminDateWidget


class ClientForm(ModelForm):
    """
    Class representing form for creating or editing Client object
    """
    class Meta:
        model = Client
        fields = "__all__"


class PhoneForm(ModelForm):
    """
    Class representing form for creating or editing Phone object
    """
    class Meta:
        model = Phone
        fields = ['number']


PhoneInlineFormset = inlineformset_factory(Client, Phone, fields=['number'], extra=1)
EmailInlineFormset = inlineformset_factory(Client, Email, fields=['email_address'], extra=1)


class ProjectForm(ModelForm):
    """
    Class representing form for creating or editing Project object

    Attributes:
        start_date: DateTime-based field for choosing date of project start
        end_date: DateTime-based field for choosing date of project end
    """
    start_date = DateTimeField(widget=AdminDateWidget())
    end_date = DateTimeField(widget=AdminDateWidget(), required=False)

    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'price']

    def clean_end_date(self):
        """
        Function for validating end_date value
        Args:
            self: Project model object
        Returns:
             (bool) True if end_data is valid
        Raises:
            Validation error if end_data is invalid
        """
        end_data = self.cleaned_data['end_date']
        start_data = self.cleaned_data['start_date']

        # Проверка того, что дата не выходит за "нижнюю" границу (не в прошлом).
        if end_data and start_data and end_data <= start_data:
            raise ValidationError(_('Некорректная дата окончанчания проекта! Дата окончания должна быть позже даты начала!'))
        return end_data
