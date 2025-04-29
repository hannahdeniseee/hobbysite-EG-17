from .models import Thread, ThreadCategory, Comment
from .forms import CommentForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import redirect
from django.urls import reverse


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
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        t = self.object
        context['other_threads'] = Thread.objects.filter(
            category=t.category).exclude(pk=t.pk)
        context['other_comments'] = Comment.objects.filter(
            thread=t).order_by('created_on')
        context['commentform'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = self.object
            comment.author = request.user.profile
            comment.save()
            return redirect(reverse('forum:thread-detail',
                                    kwargs={'pk': self.object.pk}))
        context = self.get_context_data(commentform=form)
        return self.render_to_response(context)
