from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer

class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('first_name' , 'last_name','username', 'email', 'password1', 'password2')

class CustomerForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        fields = ('address','phone')

class SearchForm(forms.Form):
    searc = forms.CharField(
            widget=forms.TextInput(
                    attrs={
                        "class": "form-control", 
                        "placeholder": "Seaerch Here"
                    }
                    )
    )