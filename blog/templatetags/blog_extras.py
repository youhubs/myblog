from django import template
from django.db.models.aggregates import Count
from django.db.models.functions import ExtractYear, ExtractMonth

from ..models import Post, Category, Tag

register = template.Library()


@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_posts': Post.objects.all().order_by('-created_at')[:num],
    }


@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    dates = Post.objects.annotate(year=ExtractYear(
        'created_at'), month=ExtractMonth('created_at')).values(
            'year', 'month').order_by('year', 'month').annotate(num_posts=Count('id'))
    return {
        'dates': dates,
    }


@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    categories = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'categories': categories,
    }


@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tags = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'tags': tags,
    }
