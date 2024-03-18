
from django.contrib.auth.forms import AuthenticationForm
from django import forms  
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.urls import reverse_lazy
from ecomWebApp.models import *
User = get_user_model()



class adminLoginForm(AuthenticationForm):
    email = forms.EmailField(label='Email')     
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['username']  


class OtpMatchForm(forms.Form):
    otp = forms.CharField()
    
class forgotPasswordForm(forms.Form):
    new_password = forms.CharField()
    cnf_new_password = forms.CharField()


class addCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent']

class AddTagsForm(forms.ModelForm):
    class Meta:
        model = Tags
        fields = ['name']

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'image', 'stock', 'price']
   