from django import forms
from .models import Review, Order
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .validators import validate_belarus_phone, validate_age_18_plus

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['departure_date']
        widgets = {
            'departure_date': forms.DateInput(attrs={'type': 'date'}),
        }


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)

    patronymic = forms.CharField(max_length=100, required=False)
    address = forms.CharField(max_length=255, required=True)

    phone = forms.CharField(
        max_length=20,
        required=True,
        validators=[validate_belarus_phone],
        help_text="+375 (XX) XXX-XX-XX",
        widget=forms.TextInput(attrs={'placeholder': '+375 (29) 123-45-67'})
    )

    birth_date = forms.DateField(
        required=True,
        validators=[validate_age_18_plus],
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')