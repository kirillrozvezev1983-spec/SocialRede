from django import forms
from django.contrib.auth.models import User
from .models import Profile, Post

class RegisterForm(forms.Form):
    name = forms.CharField(max_length=100, label='Имя')
    username = forms.CharField(max_length=150, label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    age = forms.IntegerField(min_value=1, max_value=120, label='Возраст')
    work = forms.CharField(max_length=100, required=False, label='Работа')
    hobbies = forms.CharField(max_length=200, required=False, label='Увлечения')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']
        labels = {'text': 'Что у вас нового?'}
        widgets = {'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напишите пост...'})}
