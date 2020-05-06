from .constants import Const
from django import forms
from django.core.exceptions import ValidationError
from .models import PaSettingsVacancies, PaSettingsResumes
import random



class SettingsFormVacancies(forms.ModelForm):
    class Meta:
        model = PaSettingsVacancies

        fields = ('url_base', 'query', 'page', 'threads', 'show_items', 'region')
        labels = {'url_base': ('URL'),
        'query': ('Ключевое слово'),
        'page': ('С какой страницы парсить?'),
        'threads': ('Сколько потоков подключать?'),
        'show_items': ('Сколько вакансий показать на странице?'),
        'region': ('В каком регионе?'),
        }
        widgets = {
                'url_base': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': f'URL {random.choice(Const.emj_list)}'}),

                'query': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': f'Python {random.choice(Const.emj_list)}'}),

                'page': forms.TextInput(attrs={
                    'class': 'form-control'}),

                'threads': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'min': '1',
                    'max': '50'}),

                'show_items': forms.TextInput(attrs={
                    'class': 'form-control'}),

                'region': forms.TextInput(attrs={
                    'class': 'form-control'}),
                }


class SettingsFormResumes(forms.ModelForm):
    class Meta:
        model = PaSettingsResumes

        fields = ('url_base', 'query', 'page', 'threads', 'show_items', 'region')
        labels = {'url_base': ('URL'),
        'query': ('Ключевое слово'),
        'page': ('С какой страницы парсить?'),
        'threads': ('Сколько потоков подключать?'),
        'show_items': ('Сколько резюме показать на странице?'),
        'region': ('В каком регионе?'),
        }
        widgets = {
                'url_base': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': f'URL {random.choice(Const.emj_list)}'}),

                'query': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': f'Python {random.choice(Const.emj_list)}'}),

                'page': forms.TextInput(attrs={
                    'class': 'form-control'}),

                'threads': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'min': '1',
                    'max': '50'}),

                'show_items': forms.TextInput(attrs={
                    'class': 'form-control'}),

                'region': forms.TextInput(attrs={
                    'class': 'form-control'}),
                }