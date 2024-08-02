from django.urls import path
from . import views

urlpatterns = [
    path('verify_email/', views.activation_user_email),
    path('forget_password/', views.forget_password),
    path('confirm_verify_code_reset_password/', views.confirm_verify_code_reset_password),
    path('reset_password/', views.reset_password),
]