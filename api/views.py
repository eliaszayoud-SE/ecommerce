from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from .random import generate_random_verify_code
from .models import *


@api_view(['POST'])
def activation_user_email(request):
    user_email = request.data['email']
    
    verify_code = request.data['verify_code']

    user = CustomUser.objects.get(email=user_email)

    if user.verify_code == verify_code:
        user.is_active = True
        user.save()
        print('done')
        return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)

    print('Invalid')
    return Response({'message': 'Invalid verify_code.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def forget_password(request):
    email = request.data['email']

    user = CustomUser.objects.filter(email=email).first()
    if user is not None :
        user.verify_code = generate_random_verify_code()
        user.save()
        subject = 'welcome to our ecommerce'
        message = f'Hi {user.username}, this is your new verify code  {user.verify_code} \n please use it to reset your  password'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail( subject, message, email_from, recipient_list )
        return Response({'message': 'verify code send successfully.'},status=status.HTTP_200_OK)
    
    return Response({'message': 'invalid email check if it.'},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def confirm_verify_code_reset_password(request):
    user_email = request.data['email']
    
    verify_code = request.data['verify_code']

    user = CustomUser.objects.filter(email=user_email, verify_code=verify_code).first()
    if user is not None  :
        return Response({'message': 'confirm verify code.'},status=status.HTTP_200_OK)

    return Response({'message': 'Invalid verify_code or email .'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def reset_password(request):
    user_email = request.data['email']
    
    verify_code = request.data['verify_code']

    password = request.data['password']

    user = CustomUser.objects.filter(email=user_email, verify_code=verify_code).first()
    
    if user is not None:
        user.set_password(password)
        user.save()
        return Response({'message': 'Reset password is Done.'},status=status.HTTP_200_OK)
    
    return Response({'message': 'something get wrong please try again letter.'},status=status.HTTP_400_BAD_REQUEST)



