"""
Django views for handling article-related pages.
"""

from django.shortcuts import redirect
from .models import Article, ArticleCategory, Comment, Gallery
from .forms import ArticleForm, UpdateForm, CommentForm, GalleryForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


class ArticleListView(ListView):
    """View that displays all articles and user articles."""

    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        """Function that gets extra context not in Article."""

        context = super().get_context_data(**kwargs)
        context['categories'] = ArticleCategory.objects.all()
        return context


class ArticleDetailView(DetailView):
    """View that displays the content of each article."""

    model = Article
    template_name = 'article_detail.html'

    def get_context_data(self, **kwargs):
        """Function that gets extra context not in Article."""

        context = super().get_context_data(**kwargs)
        current_article = self.get_object()
        context['articles'] = Article.objects.filter(
            author=current_article.author
        ).exclude(pk=current_article.pk)
        context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.filter(
            article=current_article)
        context['gallery_form'] = GalleryForm()
        context['gallery_images'] = Gallery.objects.filter(
            article=current_article)
        return context

    def post(self, request, *args, **kwargs):
        """Function that handles the forms in Detail View."""

        self.object = self.get_object()
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object
            comment.author = self.request.user.profile
            comment.save()

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

        return redirect('blog:article_detail', pk=self.object.pk)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """View that displays the create form."""

    model = Article
    form_class = ArticleForm
    template_name = 'article_form.html'

    def form_valid(self, form):
        """Function that checks if the editor is authorized to
        create and edit articles."""

        form.instance.author = self.request.user.profile
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    """View that displays the update form."""

    model = Article
    form_class = UpdateForm
    template_name = 'article_form.html'
