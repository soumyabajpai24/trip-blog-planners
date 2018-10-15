from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

class Myuser(models.Model):
    Username=models.CharField(max_length=50,unique=True)
    email=models.EmailField(unique=True)
    phone_val=RegexValidator(regex=r'\d{10}',message="invalid number")
    phone=models.CharField(validators=[phone_val],max_length=10)
    password=models.CharField(max_length=50)
    agent=models.BooleanField()

    def __str__(self):
        return self.Username


def validate_file_extension(value):
    if not value.name.endswith('.jpg'):
        raise ValidationError(u'upload correct format')


class Trip(models.Model):
    u_id=models.ForeignKey(Myuser,on_delete=models.CASCADE)
    slug=models.SlugField(max_length=100,unique=True)
    duration=models.PositiveIntegerField()
    date=models.DateField()
    image=models.FileField(validators=[validate_file_extension])
    discription=models.TextField(max_length=1000)

    def __str__(self):
        return self.slug
    def get_absolute_url(self):
        return redirect('myapp:userhome')

class Package(models.Model):
    u_id=models.ForeignKey(Myuser,on_delete=models.CASCADE)
    slug=models.SlugField(max_length=50)
    location=models.CharField(max_length=50)
    price=models.PositiveIntegerField()
    duration=models.PositiveIntegerField()
    description=models.TextField()
    image=models.FileField(validators=[validate_file_extension])

    def __str__(self):
        return self.slug+"  "+self.location