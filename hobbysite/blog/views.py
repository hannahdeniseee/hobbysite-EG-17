"""
Django views for handling article-related pages.
"""

from django.shortcuts import redirect
from .models import Article, ArticleCategory, Comment
from .forms import ArticleForm, UpdateForm, CommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ArticleCategory.objects.all()
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_article = self.get_object()
        context['articles'] = Article.objects.filter(
            author=current_article.author
        ).exclude(pk=current_article.pk)
        context['form'] = CommentForm()
        context['comments'] = Comment.objects.filter(
            article=current_article)
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object
            comment.author = self.request.user.profile
            comment.save()
            return redirect('blog:article_detail', pk=self.object.pk)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = UpdateForm
    template_name = 'article_form.html'
