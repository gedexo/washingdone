from django import forms
from django.forms.widgets import (EmailInput, NumberInput, RadioSelect, Select,
                                  Textarea, TextInput)

from .models import Order, OrderItem, Review


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = [
            "user_session",
        ]
        widgets = {
            "quantity": NumberInput(attrs={"min": "1", "placeholder": "Your Name"}),
            "unit": RadioSelect(),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ["user_session", "order_id", "items", "order_date", "status"]
        widgets = {
            "name": TextInput(attrs={"placeholder": "Your Name"}),
            "phone": TextInput(attrs={"placeholder": "Your Phone"}),
            "address": Textarea(attrs={"placeholder": "Address"}),
            "pincode": NumberInput(
                attrs={"placeholder": "Postcode / Zip", "max": "999999"}
            ),
            "state": Select(attrs={"placeholder": "state"}),
            "notes": Textarea(attrs={"placeholder": "notes"}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ["approved", "product"]
        widgets = {
            "name": TextInput(attrs={"id": "r-name", "placeholder": "Your Name"}),
            "email": EmailInput(attrs={"id": "r-email", "placeholder": "Your Name"}),
            "message": Textarea(
                attrs={"id": "r-textarea", "placeholder": "Your Review"}
            ),
        }
