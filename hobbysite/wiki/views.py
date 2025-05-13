from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import Article, ArticleCategory, Comment, Gallery
from .forms import ArticleForm, UpdateForm, CommentForm, GalleryForm


class ArticleListView(ListView):
    model = Article
    template_name = 'wiki/articles.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            user_articles = Article.objects.filter(author=user.profile)
            other_articles = Article.objects.exclude(author=user.profile)
        else:
            user_articles = None
            other_articles = Article.objects.all()

        context['articlecategories'] = ArticleCategory.objects.all()
        context['user_articles'] = user_articles
        context['other_articles'] = other_articles

        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'wiki/article.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()

        # Related articles (exclude current article)
        related_articles = Article.objects.filter(
            author=article.author
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

        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object
            comment.author = self.request.user.profile
            comment.save()
            form = CommentForm()  # Reset form after successful submission

        images = request.FILES.getlist('image')
        for img in images:
            Gallery.objects.create(article=self.object, image=img)

        remove_image = request.POST.get('remove_image')
        if remove_image:
            image = Gallery.objects.get(
                id=remove_image,
                article=self.object
            )
            if image.article.author.user == request.user:
                image.delete()

        return redirect('article_detail', pk=self.object.pk)


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
