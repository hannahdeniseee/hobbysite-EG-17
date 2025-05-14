"""
This is the views file to create and specify the views for the Forum app.
This includes the list view, detail view, create view, and
update view for threads.
"""

from .models import Thread, ThreadCategory, Comment
from .forms import CommentForm, ThreadForm, UpdateForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect
from django.urls import reverse


class ThreadListView(ListView):
    """
    Displays a list of all threads in the forum.

    Adds all thread categories to the context for filtering or display.
    """
    model = Thread
    template_name = 'forum/threads_list.html'
    context_object_name = 'threads'
    extra_context = {
        "threadcategories": ThreadCategory.objects.all()
    }


class ThreadDetailView(DetailView):
    """
    Displays the detail page for a single thread.

    Includes related threads in the same category, existing comments,
    and a comment submission form. Handles new comment submissions via POST.
    """
    model = Thread
    template_name = 'forum/thread_detail.html'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        """
        Adds other threads from the same category, existing comments,
        and the comment form to the context.
        """
        context = super().get_context_data(**kwargs)
        t = self.object
        context['other_threads'] = Thread.objects.filter(
            category=t.category).exclude(pk=t.pk)
        context['other_comments'] = Comment.objects.filter(
            thread=t).order_by('created_on')
        context['commentform'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles the submission of a new comment.

        If the form is valid, associates the comment with the thread and user.
        Redirects back to the same thread detail page
        with the updated comment section.
        """
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


class ThreadCreateView(LoginRequiredMixin, CreateView):
    """
    Provides a form for logged-in users to create a new thread.

    Automatically sets the thread author to the current user's profile.
    """
    model = Thread
    form_class = ThreadForm

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


class ThreadUpdateView(LoginRequiredMixin, UpdateView):
    """
    Provides a form for logged-in users to edit a thread made by them.
    """
    model = Thread
    form_class = UpdateForm
    template_name = 'forum/thread_form.html'
