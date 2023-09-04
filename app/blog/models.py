from django.db import models
from ..authors.models import User
from ckeditor.fields import RichTextField
from django.utils.text import slugify

class BlogPost(models.Model):
    title = models.CharField(max_length=2000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured_image = models.ImageField(upload_to='blog/images', null=True, blank=True)
    content = RichTextField()
    slug = models.SlugField(null=True, blank=True)
    likes_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    @property
    def author_details(self):
        author = self.author
        try:
            profile_image = author.profile_picture.url
        except:
            profile_image = None
        return {
            "id": author.id,
            "profile_image": profile_image,
            "username": author.username,
        }
    
    def save(self, *args, **kwargs):
        
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
