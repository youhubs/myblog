import markdown
import re
from markdown.extensions.toc import TocExtension
from pure_pagination.mixins import PaginationMixin

from django.utils.text import slugify
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect

from .models import Post, Category, Tag
from .forms import ContactForm


class IndexView(PaginationMixin, ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    paginate_by = 5


class FullView(PaginationMixin, ListView):
    model = Post
    template_name = 'full_view.html'
    context_object_name = 'posts'
    paginate_by = 5


class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super().get_queryset().filter(created_at__year=year, created_at__month=month)


class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


class PostDetailView(DetailView):
    model = Post
    template_name = 'detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        post.content = md.convert(post.content)

        m = re.search(
            r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''
        return post


def search(request):
    q = request.GET.get('query_item')
    if not q:
        error_msg = "Please input your search item!"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('posts:index')
    posts = Post.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
    return render(request, 'index.html', {'posts': posts})


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        msg = 'Success! Thank you for your message.'
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['huxy99@yahoo.com'])
            except BadHeaderError:
                msg = 'Invalid header found.'
                messages.add_message(request, messages.ERROR, msg, extra_tags='danger')
            messages.add_message(request, messages.SUCCESS, msg, extra_tags='success')
    return render(request, "contact.html", {'form': form})


if __name__ == "__main__":
    pass
