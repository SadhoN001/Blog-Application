from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICE =(
        ('Draft', 'Draft'),
        ('Published', 'Published'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, max_length=250)
    content = RichTextField()
    status = models.CharField(max_length=20, choices= STATUS_CHOICE, default='Draft')
    featured_img = models.ImageField(upload_to='post_imgs/', blank=True, null= True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    liked_user = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.liked_user.count()
    
class Comment(models.Model):
    body = RichTextField()
    post = models.ForeignKey(Post, on_delete= models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.body