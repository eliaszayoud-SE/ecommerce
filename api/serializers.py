from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from django.db import transaction, IntegrityError
from django.core.mail import send_mail
from django.contrib.auth import  get_user_model
from django.conf import settings


# from rest_framework import serializers
# from .models import UserProfile

User = get_user_model()

class UserCreateSerializer(BaseUserCreateSerializer):
    
    def create(self, validated_data):
        try:
           with transaction.atomic():
               user = User.objects.create_user(**validated_data)
            #    print(user.verify_code)
            #    print('=============================================')
               subject = 'welcome to our ecommerce'
               message = f'Hi {user.username}, thank you for registering this is your verify code {user.verify_code} \n please verify your email to continue use the app'
               email_from = settings.EMAIL_HOST_USER
               recipient_list = [user.email, ]
               send_mail( subject, message, email_from, recipient_list )
        except IntegrityError:
            self.fail("cannot_create_user")

        return user
    
