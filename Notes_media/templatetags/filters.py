from django import template
from django.db.models import Count

register = template.Library()

@register.filter
def sort_by_likes(posts):
    return posts.annotate(like_count=Count('like')).order_by('-like_count')