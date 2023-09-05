# #import packages
# from django.db import models
# from django.template.loader import render_to_string
# from django.core.mail import send_mail
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission

# #model manager to handle superuser and user(author) account
# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('Users must have an email address')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)

#         # Check if the user has the role of "author" and assign the "author" group
#         if user.role == 'author':
#             author_group, created = Group.objects.get_or_create(name='author')
#             user.groups.add(author_group)

#         user.save(using=self._db)
#         return user
        
#     def create_superuser(self, email, password=None, **extra_fields):
#         user = self.create_user(email, password, **extra_fields)
#         user.role == "admin"
#         user.is_superuser = True
#         user.save()
#         return user
        

# class User(AbstractBaseUser, PermissionsMixin):    
#     user_roles= [('author', 'author'), ('admin', 'admin')]

#     username = models.CharField(max_length=255, unique=True)
#     email = models.EmailField(unique=True)
#     full_name = models.CharField(max_length=100)
#     profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
#     bio = models.TextField(blank=True)
#     date_of_birth = models.DateField(null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#     role = models.CharField(max_length=50, choices= user_roles, default='author')
#     date_joined = models.DateTimeField(auto_now_add=True)
#     user_permissions = models.ManyToManyField(Permission, blank=True, related_name='user_permissions')
#     groups = models.ManyToManyField(Group, blank=True, related_name='custom_user_set', related_query_name='custom_user')

#     USERNAME_FIELD = 'username'		
#     REQUIRED_FIELDS = ['full_name', 'email']

#     objects = UserManager()

    

#     def __str__(self):
#         return self.username

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission, Group
class UserManager(BaseUserManager):
    """Create super user"""

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


class User(AbstractBaseUser, PermissionsMixin):    
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
        self.phone
        return self.email