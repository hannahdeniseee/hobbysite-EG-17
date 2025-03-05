from django.shortcuts import render
from .models import Post, PostCategory

def threads_list(request):
    ctx = {
        "posts": Post.objects.all(),
        "postcategories": PostCategory.objects.all()
    }
    return render(request, 'forum/threads_list.html', ctx)


def thread_detail(request, pk):
    ctx = {
        "post": Post.objects.get(pk=pk),
    }
    return render(request, 'forum/thread_detail.html', ctx)
