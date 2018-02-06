from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=64)
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not 'gmail.com' in email:
            raise forms.ValidationError("The email must be on gmail!")
        return email


class RegisterForm(forms.Form):
    user_name   = forms.CharField(max_length=24)
    first_name  = forms.CharField(max_length=32)
    last_name   = forms.CharField(max_length=32)
    email       = forms.EmailField()
    password    = forms.CharField(widget=forms.PasswordInput)
    password2   = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        qs = User.objects.filter(username=user_name)
        if qs.exists():
            raise forms.ValidationError("User Exist YA ROH OMAK!")
        return user_name

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if not password == password2:
            raise forms.ValidationError("Make sure you wrote the same password twice!")

        return password2


class UserLogin(forms.Form):
    user_name = forms.CharField(max_length=64)
    password  = forms.CharField(widget = forms.PasswordInput)
