from django.db import models
from account.models import User

""" Users are either authors or admins of the blog. so it makes sense to use a proxy model from Users for authors
since AUthors are still admin"""

class AuthorProjectManager(models.Manager):
   def get_queryset(self):
        return super().get_queryset().filter(role='author')

class Author(User):
    objects = AuthorProjectManager()

    class Meta:
        managed = False
        auto_created = False
        proxy = True
        verbose_name_plural = "Authors"

