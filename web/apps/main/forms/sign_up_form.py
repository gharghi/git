from django import forms
from django.contrib.auth.forms import UserCreationForm
from web.apps.jwt_store.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='لطفا یک ایمیل صحیح وارد کنید.')
    tel = forms.NumberInput()
    national_id = forms.NumberInput()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'tel', 'first_name', 'last_name')