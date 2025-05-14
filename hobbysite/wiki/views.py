from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect
from .models import Article, ArticleCategory, Comment
from .forms import ArticleForm, UpdateForm, CommentForm
from django.views.generic import View


class ArticleListView(ListView):
    model = Article
    template_name = 'wiki/articles.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        categories = ArticleCategory.objects.all()

        if user.is_authenticated:
            # Separate your articles and others'
            user_articles = Article.objects.filter(author=user.profile)
            other_articles = Article.objects.exclude(author=user.profile)

            # Group each by category
            grouped_user_articles = []
            grouped_other_articles = []
            no_category_userarticles = []
            no_category_otherarticles = []

            for category in categories:
                grouped_user_articles.append({
                    'category': category,
                    'articles': user_articles.filter(category=category)
                })
                grouped_other_articles.append({
                    'category': category,
                    'articles': other_articles.filter(category=category)
                })
            
            # Handle "Uncategorized" articles
            no_category_userarticles.append({
                'category': "Uncategorized",
                'articles': user_articles.filter(category__isnull=True)
            })
            no_category_otherarticles.append({
                'category': "Uncategorized",
                'articles': other_articles.filter(category__isnull=True)
            })

            context['grouped_user_articles'] = grouped_user_articles
            context['grouped_other_articles'] = grouped_other_articles
            context['no_category_userarticles'] = no_category_userarticles
            context['no_category_otherarticles'] = no_category_otherarticles
            context['has_user_articles'] = user_articles.exists()
            context['has_other_articles'] = other_articles.exists()
            context['is_logged_in'] = True

        else:
            # Everyone's articles in one group
            all_articles = Article.objects.all()
            grouped_all_articles = []
            nocategory_all_articles = []

            for category in categories:
                grouped_all_articles.append({
                    'category': category,
                    'articles': all_articles.filter(category=category)
                })
            
            # Handle "Uncategorized" articles
            nocategory_all_articles.append({
                'category': "Uncategorized",
                'articles': all_articles.filter(category__isnull=True)
            })

            context['grouped_all_articles'] = grouped_all_articles
            context['nocategory_all_articles'] = nocategory_all_articles
            context['has_all_articles'] = all_articles.exists()
            context['is_logged_in'] = False

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
            category=article.category
        ).exclude(pk=article.pk)[:2]

        context['related_articles'] = related_articles
        context['comments'] = Comment.objects.filter(article=article)

        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()

        context['is_owner'] = self.request.user == article.author.user
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

        return redirect('wiki:article_detail', pk=self.object.pk)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'wiki/article_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = UpdateForm
    template_name = 'wiki/article_form.html'
