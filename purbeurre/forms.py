#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from django import forms
from .models.categories import Categories


class SearchForm(forms.Form):
    """
    Product search form
    """

    name = forms.CharField(
        label="Recherche",
        widget=forms.TextInput(attrs={'placeholder': 'Nom du produit',
                                      'class': 'form-control ',
                                      'autocomplete': 'off'})
    )

    category = forms.ModelChoiceField(queryset=Categories.objects.all()
                                      , widget=forms.Select(attrs={'class': 'form-control'})
                                      , required=False)

    nutriscore_choice = (
        ('b', "B"),
        ('c', "C"),
        ('d', "D"),
        ('e', "E")
    )
    nutriscore = forms.ChoiceField(choices=nutriscore_choice,
                                   widget=forms.Select(attrs={'class': 'form-control'})
                                   , required=False)

