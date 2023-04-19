from django import forms
from django.forms import ModelChoiceField
from .models import Country 


class ContactForm(forms.Form):
    name = forms.CharField(label='Name', required=True,max_length=100, widget=forms.TextInput(attrs={'style': 'padding-right: 60px; color: black;'}))
    last_name = forms.CharField(label='Last_name', required=True ,max_length=100, widget=forms.TextInput(attrs={'style': 'padding-right: 60px; color: black;'}))
    mobile = forms.IntegerField(label='Phone', required=True, widget=forms.NumberInput(attrs={'style': 'padding-right: 60px; color: black;'}))
    country = ModelChoiceField(queryset=Country.objects.all())
    email = forms.EmailField(label='Email', required=True, max_length=100, widget=forms.TextInput(attrs={'style': '; padding-right: 60px; color: black;'}))
    subject = forms.CharField(label='Subject ', max_length=100, widget=forms.TextInput(attrs={'style': ' padding-right: 60px; color: black;'}))
    message = forms.CharField(label='Message', widget=forms.Textarea)
    aggrement = forms.BooleanField(label=' I aggree to terms and services', required=True)


