from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from .models import Article, ArticleCategory, Comment, Gallery
from .forms import ArticleForm, UpdateForm, CommentForm, GalleryForm


class ArticleListView(ListView):
    model = Article
    template_name = 'wiki/articles.html'
    context_object_name = 'articles'
    extra_context = {
        "articlecategories": ArticleCategory.objects.all()
    }


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'wiki/article.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()

        # Related articles (exclude current article)
        related_articles = Article.objects.filter(
            category=article.category
        ).exclude(pk=article.pk)[:2]

        context['related_articles'] = related_articles
        context['comments'] = Comment.objects.filter(article=article)

        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()

        context['gallery_form'] = GalleryForm()
        context['gallery_images'] = Gallery.objects.filter(
            article=article)
        
        context['is_owner'] = self.request.user == article.author
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return self.get(request, *args, **kwargs)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object
            comment.author = self.request.user.profile
            comment.save()
            form = CommentForm()  # Reset form after successful submission

        context = self.get_context_data(comment_form=form)
        return self.render_to_response(context)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "wiki/article_form.html"
    form_class = ArticleForm
    
    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = UpdateForm
    template_name = 'wiki/article_form.html'
