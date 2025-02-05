import copy
from django.shortcuts import redirect, render
from django.views import View
from user_profile import models,forms,views
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

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
            
            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user,
                    instance=self.request.user,
                    ),
                'profileform': forms.ProfileForm(
                    data=self.request.POST or None,
                    instance=self.user_profile
                    ),
                'storeform': forms.StoreForm(
                    data=self.request.POST or None,
                    instane=self.request.store
                    ),
            }
        else:
            self.context = {
                'userform': forms.UserForm(data=self.request.POST or None),
                'profileform': forms.ProfileForm(data=self.request.POST or None),
                'storeform': forms.StoreForm(data=self.request.POST or None),
            }

        self.userform = self.context['userform']
        self.profileform = self.context['profileform']
        self.storeform = self.context['storeform']

        if self.request.user.is_authenticated:
            self.template_name = 'seller/update.html'

        self.renderizer = render(self.request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
        return self.renderizer

    def post(self, *args, **kwargs):
        views.CreateView.post()

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
        messages.success(self.request, 'User logged in successfully!')

        return redirect('product:list')

class LogoutView(View):
    def get(self, *args, **kwargs):
        cart = copy.deepcopy(self.request.session.get('cart', {}))
        logout(self.request)
        self.request.session['cart'] = cart
        self.request.session.save()
        return redirect('product:list')