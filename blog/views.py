from django.shortcuts import render


def index(request):
    context = {'title': 'first post', 'content': 'this is the first post!'}
    return render(request, 'blog/index.html', context)
