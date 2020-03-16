from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupForm(UserCreationForm):
    #email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username','password1', 'password2')



class admin_form(forms.Form):
    no_stud = forms.IntegerField()
    r_date = forms.DateTimeField()
    p_date = forms.DateTimeField()
    f_date = forms.DateTimeField()
    ra_date = forms.DateTimeField()
    pay_date = forms.DateTimeField()
    fields = ('no_stud','r_date','p_date','f_date','ra_date','pay_date')



class Preferenceform(forms.ModelForm):
    n1  = forms.CharField(max_length=40)
    n2  = forms.CharField(max_length=40)
    n3  = forms.CharField(max_length=40)

    class Meta:
        model  = User
        fields  = ('n1','n2','n3')