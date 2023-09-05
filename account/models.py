from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    """Create  user"""

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class Author(AbstractBaseUser, PermissionsMixin):    
    user_roles= [('author', 'author'), ('admin', 'admin')]
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=50, choices= user_roles, default='author')
    date_joined = models.DateTimeField(auto_now_add=True)
    

    USERNAME_FIELD = 'username'		
    REQUIRED_FIELDS = ['full_name', 'email', 'is_staff', 'role']

    objects = UserManager()

    def __str__(self):
        return self.email