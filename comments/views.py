from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.contrib import messages

from blog.models import Post
from .forms import CommentForm


@require_POST
def comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        messages.add_message(request, messages.SUCCESS,
                             'Comments completed!', extra_tags='success')
        return render(request, 'blog/detail.html', context={'post': post})
    context = {
        'post': post,
        'form': form,
    }
    messages.add_message(request, messages.ERROR,
                         'Comments failed. Please try again!', extra_tags='danger')
    return render(request, 'comments/preview.html', context=context)


if __name__ == "__main__":
    pass
