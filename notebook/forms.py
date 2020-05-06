from django import forms
from .models import NbTag, NbLine
from django.core.exceptions import ValidationError
import random

from allauth.account.forms import LoginForm, SignupForm, ChangePasswordForm
from captcha.fields import CaptchaField

#класс каптчи
class SignUp(SignupForm):
    captcha = CaptchaField(label='Are you an human')


emj_list = ['😮','😥','😐','😲','😌','😗','😜','🤔','😵','😷','😉','😞','😏','😔','🖐','🤟','🤘','🤙','🙈','🙊','🤗','😁','😄','😃']

class NbTagForm(forms.ModelForm):
    class Meta:
        model = NbTag
        fields = ['title']
        labels = {'title': ('Тег'),}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }
    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        
        return new_slug

class NbLineForm(forms.ModelForm):
    class Meta:
        model = NbLine
        fields = ('head', 'body', 'tags', 'img')
        labels = {'head': ('Заголовок'),
        'body': ('Содержание записи'),
        'tags': ('Теги'),
        'img': ('Изображение'),}
        widgets = {
                'head': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': f'Какой-то весьма интересный заголовок {random.choice(emj_list)}'}),

                'body': forms.Textarea(attrs={
                    'class': 'form-control',
                    'placeholder': f'Жалобы, заявения, предложения {random.choice(emj_list)}',
                    'style': 'padding-top: 2%;'}),

                'tags': forms.SelectMultiple(attrs={
                    'class': 'form-control'}),

                'img': forms.FileInput(attrs={
                    'class': 'form-control'}),
                }
    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        
        return new_slug