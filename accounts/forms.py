from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Account


class RegistrationForms(forms.ModelForm):

    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class':'form-control'
    }))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password',
        'class':'form-control'
    }))

    class Meta:
        model=Account
        fields=['first_name','last_name','email','phone_number','password']
    
    def clean(self):
        cleaned_data=super(RegistrationForms,self).clean()

        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('password does not match ')
    
    def __init__(self,*args,**kwargs):
        super(RegistrationForms,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='Ente your first name'
        self.fields['last_name'].widget.attrs['placeholder']='Ente your last name'
        self.fields['email'].widget.attrs['placeholder']='Ente Email'
        self.fields['phone_number'].widget.attrs['placeholder']='Ente phone number'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'


