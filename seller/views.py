import copy
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth.models import User
from seller.models import Seller
from user_profile import models,forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import StoreForm
from product.models import Product, ProductVariation
from django.views.generic import DetailView,ListView
from product.forms import ProductForm, ProductVariationForm, ProductVariationFormSet

# Create your views here.

class CreateView(View):
    template_name = 'seller/create.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user_profile = None

        self.cart = copy.deepcopy(self.request.session.get('cart', {}))

        if self.request.user.is_authenticated:
            self.user_profile = models.UserProfile.objects.filter(
                user=self.request.user
            ).first()
            self.store = Seller.objects.filter(
                user=self.request.user
            ).first()

            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user,
                    instance=self.request.user,
                    ),
                'profileform': forms.ProfileForm(
                    data=self.request.POST or None,
                    instance=self.user_profile,
                    ),
                'storeform': StoreForm(
                    data=self.request.POST or None,
                    instance=self.store,
                    ),
            }
        else:
            self.context = {
                'userform': forms.UserForm(data=self.request.POST or None),
                'profileform': forms.ProfileForm(data=self.request.POST or None),
                'storeform': StoreForm(data=self.request.POST or None),
            }

        self.request.session['is_seller'] = True

        self.userform = self.context['userform']
        self.profileform = self.context['profileform']
        self.storeform = self.context['storeform']

        if self.request.user.is_authenticated:
            self.template_name = 'seller/update.html'

        self.renderizer = render(self.request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
        return self.renderizer

    def post(self, *args, **kwargs):
        if not self.userform.is_valid():
            messages.error(self.request, 'There are errors in the registration form, please check that all fields have been filled in correctly!')
            return self.renderizer

        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        # User logged in
        if self.request.user.is_authenticated:
            user = get_object_or_404(User, username=self.request.user.username)
            user.username = username
            user.email = email
            if password:
                user.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            if not self.user_profile:
                self.profileform.cleaned_data['user'] = user
                profile = models.UserProfile(**self.profileform.cleaned_data)
                profile.save()
            else:
                profile = self.profileform.save(commit=False)
                profile.user = user
                profile.save()
            if not self.store:
                store = Seller(**self.storeform)
                store.user = user
                store.save()
            else:
                store = self.storeform.save(commit=False)
                store.user = user
                store.save()
        # New user
        else:
            user = self.userform.save(commit=False)
            user.set_password(password)
            user.save()

        if password:
            authenticated_user = authenticate(
                self.request,
                username=username,
                password=password
            )
            if authenticated_user:
                login(self.request, user=user)
        self.request.session['cart'] = self.cart
        self.request.session.save()

        messages.success(
            self.request,
            'Profile created or updated successfully!'
        )
        return redirect('product:list')

class UpdateView(View):
    def get(self, *args, **kwargs):
        return redirect('seller:create')

class LoginView(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.error(self.request, 'Username and password are required!')
            return redirect('seller:create')

        authenticated_user = authenticate(
            self.request,
            username=username,
            password=password
        )

        if not authenticated_user:
            messages.error(self.request, 'Invalid username or password!')
            return redirect('seller:create')

        login(self.request, user=authenticated_user)
        self.request.session['is_seller'] = True
        messages.success(self.request, 'User logged in successfully!')

        return redirect('product:list')

class LogoutView(View):
    def get(self, *args, **kwargs):
        cart = copy.deepcopy(self.request.session.get('cart', {}))
        logout(self.request)
        self.request.session['cart'] = cart
        self.request.session.save()
        return redirect('product:list')

class DetailProductView(View):
    template_name = 'seller/detail.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.cart = copy.deepcopy(self.request.session.get('cart', {}))
        self.product = Product.objects.filter(seller_id = self.request.user.pk,id=self.kwargs['pk']).first()
        self.variation_formset = ProductVariationFormSet(data=self.request.POST or None, instance=self.product)
        self.variation = ProductVariation.objects.filter(product=self.product.pk).first()

        if self.product:
            self.context = {
                'productform': ProductForm(
                    data=self.request.POST or None,
                    instance=self.product,
                    ),
                'variation_formset': self.variation_formset,
            }
        else:
            self.context = {
            'productform':ProductForm(data=self.request.POST or None),
            'variation_formset': self.variation_formset,
        }
        self.productform = self.context['productform']
        self.request.session['is_seller'] = True

        self.renderizer = render(self.request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
        return self.renderizer

    def post(self, *args, **kwargs):
        if not self.productform.is_valid():
            messages.error(self.request, 'There are errors in the form, please check that all fields have been filled in correctly!')
            return self.renderizer

        user = User.objects.filter(id=self.request.user.pk).first()
        seller = Seller.objects.filter(user=user.pk).first()

        # Update Product
        if self.product:
            product = get_object_or_404(Product,seller_id = self.request.user.pk,id=self.kwargs['pk'])
            product = self.productform.save(commit=False)  # Evita salvar diretamente
            product.save()  # Salva no banco de dados
            self.variation_formset.instance = self.product
            self.variation_formset.save()
        # New product
        else:
            product = Product(**self.productform)
            product.seller_id = seller
            product.save()
            self.variation_formset.instance = self.product
            self.variation_formset.save()

        self.request.session['cart'] = self.cart
        self.request.session.save()

        messages.success(
            self.request,
            'Product created or updated successfully!'
        )
        return redirect('seller:detail',self.kwargs['pk'])

class DispatchLoginRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request, "You need to login to continue")
            return redirect('profile:create')
        return super().dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(seller_id=self.request.user.pk)
        return qs

class ListProductsView(DispatchLoginRequiredMixin,ListView):
    model = Product
    template_name = 'seller/list.html'
    context_object_name = 'products'
    paginate_by = 10
    ordering = ['-id']