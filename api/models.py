from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser
from .random import generate_random_verify_code

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone']
    objects = CustomUserManager()
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts." ))
    
    verify_code = models.CharField(default=generate_random_verify_code, max_length=5)
    phone = models.CharField(max_length=30, unique=True)
    is_delivery = models.BooleanField(default=False)

    def __str__(self):
        return self.email























# from django.db import models

# from django.contrib.auth.models import BaseUserManager, AbstractUser

# class CustomUserManager(BaseUserManager):
#     """
#     Custom user model manager where email is the unique identifiers
#     for authentication instead of usernames.
#     """
#     def create_user(self, email, password, **extra_fields):
#         """
#         Create and save a user with the given email and password.
#         """
#         if not email:
#             raise ValueError(_("The Email must be set"))
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user

#     def create_superuser(self, email, password, **extra_fields):
#         """
#         Create and save a SuperUser with the given email and password.
#         """
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#         extra_fields.setdefault("is_active", True)

#         if extra_fields.get("is_staff") is not True:
#             raise ValueError(("Superuser must have is_staff=True."))
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError(("Superuser must have is_superuser=True."))
#         return self.create_user(email, password, **extra_fields)


# class User(AbstractUser):
#     email = models.EmailField(unique=True)
#     first_name = None
#     last_name = None
#     is_active = models.BooleanField(default=False)
#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     def __str__(self):
#         return self.username


# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     phone = models.CharField(max_length=30)
#     verify_code = models.IntegerField(null=True, blank=True)


