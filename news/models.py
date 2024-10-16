from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blog (models.Model):
    title = models.CharField(max_length = 250)
    description = models.CharField(max_length = 250, null=True, blank=True)
    body = models.TextField()
    image = models.ImageField(upload_to ='blog')
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    Created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __str__(self):
        return f"{self.title} created on {self.Created_at}"

class Comment (models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE)
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __str__(self):
        return f"{self.owner.username}'S commet on {self.blog.title} on {self.created_at}"
class Contact (models.Model):
    name = models.CharField(max_length = 250)
    email = models.EmailField()
    message = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return f'message from {self.name} on {self.created_at}'
       
