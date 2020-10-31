#! usr/bin/env python3
# -*- Coding: UTF-8 -*-

from django import forms
from .models.categories import Categories


class SearchForm(forms.Form):
    """
    Product search form
    """
    research = forms.CharField(
        label="Recherche",
        widget=forms.TextInput(attrs={'placeholder': 'Nom de aliment',
                                      'class': 'form-control ',
                                      'autocomplete': 'off'})
    )


class FilterForm(forms.Form):
    """
    Product search form with filters
    """

    name = forms.CharField(
        label="Recherche",
        widget=forms.TextInput(attrs={'placeholder': 'Trouvez un aliment',
                                      'class': 'form-control ',
                                      'autocomplete': 'off'})
    )

    category = forms.ModelChoiceField(queryset=Categories.objects.all()
                                      , widget=forms.Select(attrs={'class': 'form-control'}))

    nutriscore_choice = (
        ('b', "B"),
        ('c', "C"),
        ('d', "D"),
        ('e', "E")
    )
    nutriscore = forms.ChoiceField(choices=nutriscore_choice,
                                   widget=forms.Select(attrs={'class': 'form-control'})
                                   )
