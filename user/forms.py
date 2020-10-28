#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UsernameField


class LoginForm(forms.Form):
    """
    Login form
    """
    email = forms.EmailField(label="",
                             required=True,
                             widget=forms.TextInput
                             (attrs=
                              {'placeholder': "Adresse e-mail",
                               'class': "form-control form-control-user"
                               }))

    password = forms.CharField(label="",
                               strip=False,
                               widget=forms.PasswordInput
                               (attrs=
                                {'autocomplete': 'current-password',
                                 'class': "form-control form-control-user",
                                 'placeholder': "Mot de passe"}))


class UserRegistrationForm(forms.ModelForm):
    """
    Subscription form
    """

    class Meta:
        model = User
        fields = ('email', 'first_name')

    first_name = forms.CharField(label='',
                                 widget=forms.TextInput
                                 (attrs=
                                  {'placeholder': "Prénom",
                                   'class': "form-control form-control-user"}))

    password = forms.CharField(label='',
                               strip=False,
                               widget=forms.PasswordInput
                               (attrs=
                                {'placeholder': "Mot de passe",
                                 'class': "form-control form-control-user"}))
    password2 = forms.CharField(label='',
                                widget=forms.PasswordInput
                                (attrs=
                                 {'placeholder': "Répétez votre mot de passe",
                                  'class': "form-control form-control-user"}))
    email = forms.EmailField(label="",
                             required=True,
                             error_messages={'invalid': 'Saisissez un adresse e-mail valide.'},
                             widget=forms.TextInput
                             (attrs=
                              {'placeholder': "Adresse e-mail",
                               'class': "form-control form-control-user"}))

    def clean_email(self):
        """
        Check if e-mail is already used
        """
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("Cette adresse e-mail est déjà enregistrée.")
        return self.cleaned_data['email']

    def clean_password2(self):
        """
        check if password are identical ; if its not, clean
        """
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Les mots de passe ne sont pas identiques.')
        return cd['password2']
