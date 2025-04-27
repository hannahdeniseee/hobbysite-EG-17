from .models import Thread, ThreadCategory
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


class ThreadListView(ListView):
    model = Thread
    template_name = 'forum/threads_list.html'
    context_object_name = 'threads'
    extra_context = {
        "threadcategories": ThreadCategory.objects.all()
    }


class ThreadDetailView(DetailView):
    model = Thread
    template_name = 'forum/thread_detail.html'
