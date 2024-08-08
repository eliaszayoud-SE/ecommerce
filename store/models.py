from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import  get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

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
    order = models.ForeignKey('Order', on_delete=models.CASCADE, null=True, blank=True, )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    unit_price = models.FloatField(default=0)

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

class Order(models.Model):

    ORDER_TYPE_CHOISSES = [
        (0, 'delivery'),
        (1, 'drive thru') 
    ]

    PAYMENT_METHOD_CHOISSES = [
        (0, 'cash'),
        (1, 'Card') 
    ]

    ORDER_STATUS_CHOISES = [
        (0, 'Pending Approval'),
        (1, 'The Order is Being Prepared'),
        (2, 'On the Way'),
        (3, 'The order has been delivered')
    ]

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.SmallIntegerField(choices=ORDER_TYPE_CHOISSES, default='delivery')
    price_delivery = models.IntegerField(null=True, blank=True)
    price = models.FloatField()
    payment_type = models.SmallIntegerField(choices=PAYMENT_METHOD_CHOISSES)
    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.SmallIntegerField(choices=ORDER_STATUS_CHOISES, default=0)
    date_time = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField(default=0)
    rating = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)], null=True, blank=True)
    note = models.CharField(max_length=255, null=True, blank=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=255)
    date_time = models.DateTimeField(auto_now_add=True)
