from django import forms
from django.forms.widgets import EmailInput, Textarea, TextInput

from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ("timestamp",)
        widgets = {
            "name": TextInput(
                attrs={"class": "required form-control", "placeholder": "Your Name"}
            ),
            "phone": TextInput(
                attrs={"class": "required form-control", "placeholder": "Your Phone"}
            ),
            "place": TextInput(
                attrs={"class": "required form-control", "placeholder": "Your Location"}
            ),
            "email": EmailInput(
                attrs={
                    "class": "required form-control",
                    "placeholder": "Your Email Address",
                }
            ),
            "message": Textarea(
                attrs={
                    "class": "required form-control",
                    "placeholder": "Type Your Message",
                }
            ),
        }
