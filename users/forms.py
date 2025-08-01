from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации пользователя"""

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "role", "phone", "birth_date")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class CustomAuthenticationForm(AuthenticationForm):
    """Форма входа пользователя"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class UserProfileForm(forms.ModelForm):
    """Форма редактирования профиля"""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone", "birth_date")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
