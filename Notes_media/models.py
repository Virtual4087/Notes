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
    level = models.ForeignKey(
        Level, on_delete=models.SET_NULL, related_name="users_of_this_level", null=True, blank=True
    )
    category = models.ManyToManyField(
        Category, blank=True, related_name="users_of_this_category"
    )
    following = models.ManyToManyField(
        "self", blank=True, related_name="follower", symmetrical=False
    )
    saved_post = models.ManyToManyField("Post", blank=True, related_name="saved_by")

    profile_picture = models.FileField(blank=True, upload_to="profile_pictures")

    def __str__(self):
        return self.username


class Image(models.Model):
    image = models.ImageField(upload_to="images")


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts", default=0)
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=False)
    image = models.ManyToManyField(Image, blank=True)
    file = models.FileField(blank=True, upload_to="pdf_files")
    like = models.ManyToManyField(User, blank=True, related_name="liked_posts")
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, related_name="categoty_posts", blank = True, on_delete = models.SET_NULL, null = True)
    level = models.ForeignKey(Level, related_name="level_posts", blank = True, on_delete = models.SET_NULL, null = True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comments")
    comment = models.TextField()