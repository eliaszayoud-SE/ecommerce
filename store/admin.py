from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Favorite)
admin.site.register(Cart)
admin.site.register(Address)
admin.site.register(Coupon)
admin.site.register(Order)