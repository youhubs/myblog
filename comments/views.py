import markdown
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from markdown.extensions.toc import TocExtension

from blog.models import Post

from .forms import CommentForm


@require_POST
def comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    md = markdown.Markdown(
        extensions=[
            "markdown.extensions.extra",
            "markdown.extensions.codehilite",
            TocExtension(slugify=slugify),
        ]
    )
    post.content = md.convert(post.content)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        messages.add_message(
            request, messages.SUCCESS, "Comments completed!", extra_tags="success"
        )
        return render(request, "detail.html", context={"post": post})
    context = {
        "post": post,
        "form": form,
    }
    messages.add_message(
        request,
        messages.ERROR,
        "Comments failed. Please try again!",
        extra_tags="danger",
    )
    return render(request, "comments/preview.html", context=context)


if __name__ == "__main__":
    pass
