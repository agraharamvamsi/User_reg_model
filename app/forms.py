from app.models import * 
from django import forms


class userform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        widgets = {'password' : forms.PasswordInput,
        'username':forms.TextInput(attrs = {'class':'form-control'}),
        'email':forms.TextInput(attrs = {'class':'form-control'}),
        }
        help_texts = {'username' : ""}

class profileform(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'profile_pic']

        widgets = {
            'address':forms.TextInput(attrs = {'class':'form-control'}),
        }