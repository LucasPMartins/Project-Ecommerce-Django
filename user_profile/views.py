from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.views import View
from . import models
from . import forms
import copy

class ProfileBaseView(View):
    template_name = 'user_profile/create.html'

    def setup(self, *args, **kwargs):
        super().setup( *args, **kwargs)

        self.cart = copy.deepcopy(self.request.session.get('cart', {}))

        self.user_profile = None

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
                    )
            }
        else:
            self.context = {
                'userform': forms.UserForm(data=self.request.POST or None),
                'profileform': forms.ProfileForm(data=self.request.POST or None)
            }

        self.request.session['is_seller'] = False
        self.userform = self.context['userform']
        self.profileform = self.context['profileform']

        if self.request.user.is_authenticated:
            self.template_name = 'user_profile/update.html'

        self.renderizer = render(self.request, self.template_name, self.context)

    def get(self, request, *args, **kwargs):
        return self.renderizer

class CreateView(ProfileBaseView):
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
        return redirect('profile:create')

class LoginView(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.error(self.request, 'Username and password are required!')
            return redirect('profile:create')

        authenticated_user = authenticate(
            self.request,
            username=username,
            password=password
        )

        if not authenticated_user:
            messages.error(self.request, 'Invalid username or password!')
            return redirect('profile:create')
        
        login(self.request, user=authenticated_user)
        self.request.session['is_seller'] = False
        messages.success(self.request, 'User logged in successfully!')
        return redirect('product:list')

class LogoutView(View):
    def get(self, *args, **kwargs):
        cart = copy.deepcopy(self.request.session.get('cart', {}))
        logout(self.request)
        self.request.session['cart'] = cart
        self.request.session.save()
        return redirect('product:list')

