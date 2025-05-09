from django.views.generic import ListView, DetailView, TemplateView, UpdateView, CreateView
from .models import Product, Transaction
from .forms import TransactionForm, ProductForm
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from user_management.models import Profile
from django.urls import reverse
from django.views.generic import ListView
from .models import Product


class ProductListView(LoginRequiredMixin,ListView):
    model = Product
    template_name = 'merch_list.html'
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                user_profile = Profile.objects.get(user=self.request.user)
                context['user_products'] = Product.objects.filter(owner=user_profile)
                context['other_products'] = Product.objects.exclude(owner=user_profile)
            except Profile.DoesNotExist:
                context['user_products'] = []
                context['other_products'] = Product.objects.all()
        else:
            context['user_products'] = []
            context['other_products'] = Product.objects.all()
        
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'merch_detail.html'
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_type"] = self.object.product_type
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            try:
                transaction.buyer = Profile.objects.get(user=request.user)
            except Profile.DoesNotExist:
                messages.error(request, "You must have a profile to make purchases.")
                return self.get(request, *args, **kwargs)

            transaction.product = self.object

            if transaction.amount <= self.object.stock:
                self.object.stock -= transaction.amount
                if self.object.stock == 0:
                    self.object.status = 'Out of Stock'
                self.object.save()
                transaction.save()
                return redirect('merchstore:cart')
            else:
                messages.error(request, "Not enough stock available.")
        else:
            messages.error(request, "Invalid form submission.")

        return self.get(request, *args, **kwargs)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'merch_form.html'

    def form_valid(self, form):
        try:
            profile = self.request.user.profile
            print(f"Profile found: {profile}")
        except Profile.DoesNotExist:
            messages.error(self.request, "You must have a profile to create products.")
            return redirect('accounts:register')  # Adjust to your profile creation URL
       
        print("Profile: ", profile)
        form.instance.owner = profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('merchstore:merch-detail', kwargs={'pk': self.object.pk})


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'description', 'price', 'stock', 'status', 'product_type']
    template_name = 'merch_form.html'

    def form_valid(self, form):
        if form.instance.stock == 0:
            form.instance.status = 'Out of Stock'
        else:
            form.instance.status = 'Available'
        return super().form_valid(form)


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            profile = Profile.objects.get(user=self.request.user)
            context['transactions'] = Transaction.objects.filter(buyer=profile)
        except Profile.DoesNotExist:
            context['transactions'] = []
        return context


class TransactionListView(LoginRequiredMixin, TemplateView):
    template_name = 'transactions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user_profile = Profile.objects.get(user=self.request.user)
            user_products = Product.objects.filter(owner=user_profile)
            transactions = Transaction.objects.filter(product__in=user_products)
        except Profile.DoesNotExist:
            transactions = []

        grouped = {}
        for transaction in transactions:
            buyer = transaction.buyer
            grouped.setdefault(buyer, []).append(transaction)
        context['grouped_transactions'] = grouped
        return context