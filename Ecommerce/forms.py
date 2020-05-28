from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import User , Review

# class SignUpForm(UserCreationForm):
#     email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
#     class Meta:
#         model = User
#         fields = ('first_name' , 'last_name','username', 'email', 'password1', 'password2')


class MyUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta(UserCreationForm):
        model = User
        fields = ('first_name' , 'last_name','username', 'email', 'address', 'password1', 'password2')
        required = (('first_name' , 'last_name','username', 'email', 'address', 'password1', 'password2'))

class MyUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = User
        fields = ('address', 'phone')


class SearchForm(forms.Form):
    searc = forms.CharField(
            widget=forms.TextInput(
                    attrs={
                        "class": "form-control", 
                        "placeholder": "Seaerch Here"
                    }
                    )
    )

class ReviewForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = Review
        fields = ('subject', 'comment' , 'rating')
