from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Category(models.Model):
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.category

class Level(models.Model):
    level = models.CharField(max_length=20)

    def __str__(self):
        return self.level

class User(AbstractUser):
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, related_name="users_of_this_level", null=True)
    category = models.ManyToManyField(Category, blank=True, related_name="users_of_this_category")

    def __str__(self):
        return self.username

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user_posts", null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.title}"
