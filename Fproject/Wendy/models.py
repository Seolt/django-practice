from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UploadFile(models.Model):
    
    title=models.CharField(default='no tilte', max_length=20)
    file = models.FileField(null=True)
    
    def __str__(self):
        return f'제목 : {self.title} 파일명 : {self.file}'
    
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username.strip(), email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
        ('facilitator', 'Facilitator'),
    )
    can_login = models.BooleanField(default=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    user_image = models.ImageField(upload_to='profile_image/',blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    username = models.CharField(
        max_length=150, 
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits, and spaces only.',
        validators=[],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )

    def is_facilitator(self):
        return self.user_type == 'facilitator'

    def is_student(self):
        return self.user_type == 'student'

    def is_teamlead(self):
        return self.user_type == 'teamlead'

    objects = CustomUserManager()
