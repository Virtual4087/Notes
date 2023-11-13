from django.contrib import admin
from .models import User, Post, Category, Level, Image, Comment

# Register your models here.

admin.site.register(Level)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Comment)

