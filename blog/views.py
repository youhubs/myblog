import markdown
import re

from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from django.shortcuts import render, get_object_or_404

from .models import Post, Category, Tag


def index(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'blog/index.html', context)


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])
    post.content = md.convert(post.content)

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    return render(request, 'blog/detail.html', context={'post': post})


def archive(request, year, month):
    posts = Post.objects.filter(
        created_at__year=year, created_at__month=month)
    return render(request, 'blog/index.html', context={'posts': posts})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    posts = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'posts': posts})


def tag(reques, pk):
    tag = get_object_or_404(Tag, pk=pk)
    posts = Post.objects.filter(tags=tag)
    return render(reques, 'blog/index.html', context={'posts': posts})


if __name__ == "__main__":
    pass
