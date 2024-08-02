from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import  get_user_model

User = get_user_model()

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100)
    image = models.FileField(upload_to='category/images', validators=[FileExtensionValidator(['svg'])])
    date = models.DateField(auto_now_add=True)


class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    description_ar = models.CharField(max_length=255)
    image = models.ImageField(upload_to='items/image')
    count = models.IntegerField()
    active = models.BooleanField(default=True)
    price = models.FloatField()
    discount = models.SmallIntegerField()
    date = models.DateField(auto_now_add=True)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    phone = models.CharField(max_length=30, null=True, blank=True)
    lat = models.FloatField()
    long = models.FloatField()   

class Coupon(models.Model):
    name = models.CharField(max_length=50, unique=True)
    count = models.PositiveIntegerField()
    discount = models.PositiveSmallIntegerField(default=0)
    expire_date = models.DateTimeField()

