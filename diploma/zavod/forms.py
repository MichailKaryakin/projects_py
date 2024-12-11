from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import *
import datetime


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2','first_name','last_name')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class AddPostForm(forms.ModelForm):
    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.fields['cat'].empty_label = "Категория не выбрана"

    class Meta:
        model = RequestJob
        fields = ['id_work','equipment', 'note']
        widgets = {
            'id_work': forms.Select(attrs={'class': 'form-control'}),
            'equipment': forms.Select(attrs={'class': 'form-control'}),
            'note': forms.TextInput(attrs={'cols': 60, 'rows': 10,'class': 'form-control'}),
        }

#    def clean_title(self):
#        title = self.cleaned_data['title']
#        if len(title) > 200:
#            raise ValidationError('Длина превышает 200 символов')

#        return title

class AddWork(forms.ModelForm):
    def __init__(self, *args, **kwargs):
     super(AddWork, self).__init__(*args, **kwargs)
     self.fields['id_employee'].queryset = User.objects.filter(groups__name='employee')
    class Meta:
        model = Work
        fields = ['name','duration','price', 'note','id_employee','difficult','garantiya']
        widgets = {
            'id_employee': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'note': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'garantiya': forms.TextInput(attrs={'class': 'form-control'}),
            'difficult': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AddEquipment(forms.ModelForm):
    def __init__(self, *args, **kwargs):
     super(AddEquipment, self).__init__(*args, **kwargs)
     #self.fields['id_employee'].queryset = User.objects.filter(groups__name='employee')
    class Meta:
        model = Equipment
        fields = ['mark', 'country', 'date_release','brand','model','price','garantiya','srok_sl']
        widgets = {
            'mark': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'garantiya': forms.TextInput(attrs={'class': 'form-control'}),
            'srok_sl': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'date_release': forms.DateTimeInput(attrs={'class': 'form-control',
                                                        'type': 'date',
                                                        'pattern': '\d{2}\.\d{2}\.\d{4}',
                                                        'title': 'Введите дату в формате ДД.ММ.ГГГГ'})
        }
