
from typing import Any
from django import forms


class UserLogForm(forms.Form):
    username = forms.CharField(max_length=100,error_messages={'required':'Enter Username'})
    password = forms.CharField(widget=forms.PasswordInput,error_messages={'required':'Hey! You missed Password'})
    
        
        
class UserSignForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    Repassword = forms.CharField(widget=forms.PasswordInput)
    userType = forms.CharField(error_messages={'required':'Enter type: Author or Reader'})
    
    def clean(self):
        super().clean()
        name = self.cleaned_data['username']
        if(len(name)<4):
            raise forms.ValidationError("length of the username should be 4")
        pwd = self.cleaned_data['password']
        repwd = self.cleaned_data['Repassword']        
        if pwd != repwd:
            raise forms.ValidationError("Password Mismatch")
        
