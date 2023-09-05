from django.db import models
from ..blog.models import BlogPost
from account.models import User

class BlogPostPermission(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission_type = models.CharField(max_length=20, choices=[('edit', 'Edit'), ('view', 'View')])