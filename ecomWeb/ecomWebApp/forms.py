from django.forms import fields  
from .models import *
from django import forms  
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login,authenticate

class UserForm(forms.ModelForm):  
    class Meta:  
        model = User  
        fields = ['username','email', 'mobile_number', 'password'] 
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    email = forms.EmailField(label='Email')     
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['username']  

class CartProductForm(forms.ModelForm):  
    class Meta:  
        model = CartProduct  
        fields = ['user_id', 'product_id', 'qty']  
        