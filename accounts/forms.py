from typing import Any
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.widgets import PasswordInput, TextInput
from .models import Car, Order, Answer

User = get_user_model()

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['phone_number', 'password1', 'password2']
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(UserCreateForm,self).__init__(*args, **kwargs)

        self.fields['phone_number'].label = "Номер телефона"
        self.fields['phone_number'].required = True
        self.fields['password1'].help_text = ""

    def clean_phone_number(self):
        email = self.cleaned_data['phone_number']
        if User.objects.filter(email=email).exists and len(email) > 15:
            raise forms.ValidationError("Phone must be less than 11 characters")
        return email
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Phone Number', 'class':'form-control'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password', 'class':'form-control'}))
    
class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'vin', 'car_image']
        exclude = ['user',]
        
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['car', 'name', 'component_image']
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Извлекаем пользователя и удаляем из kwargs
        super(OrderCreateForm, self).__init__(*args, **kwargs)  # Теперь kwargs не содержит неожиданный аргумент 'user'
        if user:
            # Фильтруем queryset поля 'car', оставляя только автомобили текущего пользователя
            self.fields['car'].queryset = Car.objects.filter(user=user)
            
            

class AnswerCreateForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['manufacturer', 'quality', 'guarantee', 'status', 'delivery', 'code', 'price','answer_image']
        exclude = ['user',]
        widgets = {
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'quality': forms.TextInput(attrs={'class': 'form-control'}),
            'guarantee': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'answer_image': forms.FileInput(attrs={'class': 'form-control'}),
        }