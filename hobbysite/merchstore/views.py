"""
This is the views file to create and specify the views for the Merchstore app.
This includes the list view, detail view, create view, and update view
for products and the cart and transaction views.
"""

from django.views.generic import (ListView,
                                  DetailView,
                                  TemplateView,
                                  UpdateView,
                                  CreateView)
from .models import Product, Transaction
from .forms import TransactionForm, ProductForm
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from user_management.models import Profile
from django.urls import reverse


class ProductListView(ListView):
    """
    Displays a list of all products in the merchandise store.
    """
    model = Product
    template_name = 'merch_list.html'
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        """
        Separates products owned by user from other users.
        """
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                user_profile = Profile.objects.get(user=self.request.user)
                context['user_products'] = Product.objects.filter(
                    owner=user_profile
                )
                context['other_products'] = Product.objects.exclude(
                    owner=user_profile
                )
            except Profile.DoesNotExist:
                context['user_products'] = []
                context['other_products'] = Product.objects.all()
        else:
            context['user_products'] = []
            context['other_products'] = Product.objects.all()

        return context


class ProductDetailView(DetailView):
    """
    Displays the detail page of a product.
    """
    model = Product
    template_name = 'merch_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        """
        Checks if product is not owned by user and still in stock.
        """
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        try:
            user_profile = self.request.user.profile
        except Profile.DoesNotExist:
            user_profile = None

        context['is_owner'] = product.owner == user_profile
        context['can_buy'] = (
            user_profile and product.stock > 0
            and product.owner != user_profile
        )

        if context['can_buy']:
            context['form'] = TransactionForm()

        return context

    def post(self, request, *args, **kwargs):
        """
        Checks if user is logged in.

        Checks if the quantity to be purchased by the user is valid.
        """
        self.object = self.get_object()
        product = self.object

        if not request.user.is_authenticated:
            return redirect('accounts:login')

        try:
            buyer = request.user.profile
        except Profile.DoesNotExist:
            messages.error(
                request, "You need a profile to make a transaction."
            )
            return redirect('accounts:register')

        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.product = product
            transaction.buyer = buyer

            quantity = transaction.amount
            if quantity <= 0:
                messages.error(request, "Please enter a valid amount.")
                return self.get(request, *args, **kwargs)
        
            if quantity > product.stock:
                messages.error(request, "Not enough stock available.")
                return self.get(request, *args, **kwargs)

            product.stock -= quantity
            if product.stock == 0:
                product.status = 'Out of stock'
                product.save()

            product.save()
            transaction.save()

            return redirect('merchstore:merch-cart')

        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Allows user to create a new product.
    """
    model = Product
    form_class = ProductForm
    template_name = 'merch_form.html'

    def form_valid(self, form):
        """
        Ensures the user is logged in before creating a product.
        """
        try:
            profile = self.request.user.profile
            print(f"Profile found: {profile}")
        except Profile.DoesNotExist:
            messages.error(
                self.request, "You must have a profile to create products."
            )
            return redirect('accounts:register')

        print("Profile: ", profile)
        form.instance.owner = profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'merchstore:merch-detail', kwargs={'pk': self.object.pk}
        )


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    Allows the user to update information on the product.
    """
    model = Product
    fields = ['name',
              'description',
              'price',
              'stock',
              'status',
              'product_type']
    template_name = 'merch_form.html'

    def form_valid(self, form):
        """
        Updates status of product according to quantity.
        """
        if form.instance.stock == 0:
            form.instance.status = 'Out of Stock'
        else:
            form.instance.status = 'Available'
        return super().form_valid(form)


class CartView(LoginRequiredMixin, TemplateView):
    """
    Allows users to see all items they have purchased.
    """
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        """
        Filters the products that were bought by the user.
        Computes for the total amount spent by the user.
        """
        context = super().get_context_data(**kwargs)
        user_profile = self.request.user.profile

        transactions = Transaction.objects.filter(
            buyer=user_profile
        ).select_related('product__owner')
        grand_total = sum(
            transaction.total_price for transaction in transactions
        )

        grouped_transactions = {}
        for transaction in transactions:
            seller = transaction.product.owner
            if seller not in grouped_transactions:
                grouped_transactions[seller] = []
            grouped_transactions[seller].append(transaction)

        context['grouped_transactions'] = grouped_transactions
        context['grand_total'] = grand_total
        context['messages'] = messages.get_messages(self.request)

        return context


class TransactionListView(LoginRequiredMixin, TemplateView):
    """
    Lists all of the transactions of the user.
    """
    template_name = 'transactions.html'

    def get_context_data(self, **kwargs):
        """
        Lists user's products that were purchased by other users.
        """
        context = super().get_context_data(**kwargs)
        try:
            user_profile = Profile.objects.get(user=self.request.user)
            user_products = Product.objects.filter(owner=user_profile)
            transactions = Transaction.objects.filter(
                product__in=user_products
            )
        except Profile.DoesNotExist:
            transactions = []

        grouped = {}
        for transaction in transactions:
            buyer = transaction.buyer
            grouped.setdefault(buyer, []).append(transaction)
        context['grouped_transactions'] = grouped
        return context
