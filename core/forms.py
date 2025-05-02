from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import CustomerDetail



class AuthenticateForms(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']
        labels = {'email':'Email'}
        widgets =   {
                        'username':forms.TextInput(attrs= {'class':'form-input'}),
                        'first_name':forms.TextInput(attrs={'class':'form-input'}),
                        'last_name':forms.TextInput(attrs={'class':'form-input'}),
                        'email':forms.TextInput(attrs={'class':'form-input'})
                    }
        

class CustomerForm(forms.ModelForm):
    class Meta:
        model = CustomerDetail
        fields=['name','address','city','state','pincode']
        labels ={'name':'Full Name'}
        widgets= {'name':forms.TextInput(attrs={'class':'form-control'}),
                  'address':forms.TextInput(attrs={'class':'form-control'}),
                  'city':forms.TextInput(attrs={'class':'form-control'}),
                  'state':forms.Select(attrs={'class':'form-control'}),
                  'pincode':forms.NumberInput(attrs={'class':'form-control'}),
                  }