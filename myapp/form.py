from django import forms
import re
from .models import Myuser,Trip

class Userlogin(forms.Form):
    Username_Email=forms.CharField(max_length=100)
    Password=forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        user=self.cleaned_data.get("Username_Email")
        passw=self.cleaned_data.get("Password")
        if re.search(r'\w+@+\w+.+\w',user):
            try:
                Myuser.objects.get(email=user,password=passw)
            except:
                raise forms.ValidationError("incorrect credentials")
        else:
            try:
                Myuser.objects.get(Username=user, password=passw)
            except:
                raise forms.ValidationError("incorrect credentials")

class Userregister(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=Myuser
        fields=['Username','email','phone','agent']
    def clean(self):
        pass1=self.cleaned_data.get("password")
        pass2=self.cleaned_data.get("confirm_password")
        if pass1!=pass2:
            raise forms.ValidationError("incorrect password")


class Planner(forms.Form):
    duration=forms.IntegerField()
    price=forms.IntegerField()
    location=forms.CharField(max_length=100)