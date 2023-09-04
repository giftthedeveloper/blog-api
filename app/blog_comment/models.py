from django.db import models
from ..blog.models import BlogPost

class BlogComment(models.Model):
    """ The blog comment model is responsible for storing information pertaining to a blog comment. It is not
    tied to a users as blogpost can be read by anonymous readers hence the need for commenter_name"""

    commenter_name = models.CharField(max_length=1000)
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    