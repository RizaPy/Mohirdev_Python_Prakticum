from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from accounts.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(ModelForm):
    password = forms.CharField(label='Parol', widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Parolni takrorlang', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_password_2(self):
        data = self.cleaned_data
        if data['password'] != data['password_2']:
            raise forms.ValidationError('Ikkala parol bir-biriga teng bo\'lish kerak')
        return data['password_2']

# class UserRegistrationForm(ModelForm):
#     password = forms.CharField(label='Parol', widget=forms.PasswordInput)
#     password_2 = forms.CharField(label='Parolni takrorlang', widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         fields = '__all__'
#
#     def clean_password_2(self):
#         data = self.cleaned_data
#         if data['password'] != data['password_2']:
#             raise forms.ValidationError("Ikkala parol bir-biriga teng bo'lish kerak")
#         return data['password_2']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'birth_date', 'image']

class userEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

