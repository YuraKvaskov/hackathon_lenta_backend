from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from api.v1.models import Store


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=100, required=True, help_text="Введите имя пользователя")
    last_name = forms.CharField(
        max_length=100, required=True, help_text="Введите фамилию пользователя")
    store = forms.ModelChoiceField(
        queryset=Store.objects.all(), required=True, help_text="Выберите магазин.")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'store')