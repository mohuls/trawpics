from distutils.command.upload import upload
from pyexpat import model
from statistics import mode
from django.db import models

from django.contrib.auth.models import User

class Home(models.Model):
    title = models.CharField(max_length=120)
    baseline = models.CharField(max_length=240)
    facebook = models.CharField(max_length=200)
    twitter = models.CharField(max_length=200)
    instagram = models.CharField(max_length=200)
    vemio = models.CharField(max_length=200)
    pinterest = models.CharField(max_length=200)

    def save(self,*args,**kwargs):
        if Home.objects.all().count() > 1:
            return False # or you can raise validation error
        else:
            super(Home,self).save(*args,**kwargs)

class Category(models.Model):
    name = models.CharField(max_length=30)

    at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Stock(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=256)
    detail = models.TextField(max_length=2048)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    preview = models.FileField(upload_to='uploads/stock/')
    license = models.FileField(upload_to='uploads/license/')
    download = models.FileField(upload_to='uploads/item/')

    at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    review_on = models.ForeignKey(Stock, on_delete=models.CASCADE)
    review = models.TextField(max_length=1024)
    star = models.IntegerField()
    
    at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reviewer.username


class Order(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    paid = models.IntegerField()
    expires = models.DateField()

    at = models.DateTimeField(auto_now_add=True)

class PaymentApi(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=240)