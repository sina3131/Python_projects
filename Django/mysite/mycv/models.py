from django.db import models
from django import forms


class Portfolio(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='media/')


    def __str__(self):
        return self.title
    


class Contanct(models.Model):
    name = models.CharField( max_length=100, default='')
    last_name = models.CharField( max_length=100, default='')
    mobile = models.IntegerField(default=' ')
    country = models.TextField(default=' ', max_length=100)
    email = models.EmailField( default='')
    subject = models.CharField( default='', max_length=100)
    message = models.TextField(default='')

    def __str__(self):
        return self.name
    
class Country(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


    
# class Contanct(models.Model):
#     name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'style': 'padding-right: 60px;'}))
#     last_name = forms.CharField(label='Last_name', max_length=100, widget=forms.TextInput(attrs={'style': 'padding-right: 60px;'}))
#     mobile = forms.IntegerField(label='Phone',  widget=forms.NumberInput(attrs={'style': 'padding-right: 60px;'}))
#     country = forms.CharField(label='Country', max_length=100, widget=forms.TextInput(attrs={'style': 'padding-right: 60px;'}))
#     email = forms.EmailField(label='Email', max_length=100, widget=forms.TextInput(attrs={'style': '; padding-right: 60px;'}))
#     subject = forms.CharField(label='Subject ', max_length=100, widget=forms.TextInput(attrs={'style': ' padding-right: 45px;'}))
#     message = forms.CharField(label='Message', widget=forms.Textarea)

#     def __str__(self):
#         return self.name
