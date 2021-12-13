from django.forms.models import inlineformset_factory, ModelForm
from .models import Client, Phone, Email


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = "__all__"


class PhoneForm(ModelForm):
    class Meta:
        model = Phone
        fields = ['number']


PhoneInlineFormset = inlineformset_factory(Client, Phone, fields=['number'], extra=1)
EmailInlineFormset = inlineformset_factory(Client, Email, fields=['email_address'], extra=1)
