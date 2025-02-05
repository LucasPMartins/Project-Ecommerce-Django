from django import forms
from django.contrib.auth.models import User
from . import models

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = '__all__'
        exclude = ['user']

class UserForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(required=False, widget=forms.PasswordInput, label='Confirm Password')

    def __init__(self, user=None,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password', 'password2']

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_errors = {}

        username_data = cleaned.get('username')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')
        email_data = cleaned.get('email')

        user_db = User.objects.filter(username=username_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_name_exists = 'Username already exists'
        error_email_exists = 'Email already exists'
        error_password_match = 'Password is required'

        # User logged in (update)
        if self.user:
            if username_data != self.user.username:
                if user_db:
                    validation_errors['username'] = error_name_exists
            if email_data != self.user.email:
                if email_db:
                    validation_errors['email'] = error_email_exists
        # User not logged in (create)
        else:
            if user_db:
                validation_errors['username'] = error_name_exists
            if email_db:
                validation_errors['email'] = error_email_exists
            if not password_data:
                validation_errors['password'] = 'Password is required'

        if password_data:
            if password_data != password2_data:
                validation_errors['password'] = error_password_match
                validation_errors['password2'] = error_password_match
            if len(password_data) < 8:
                validation_errors['password'] = 'Password must have at least 8 characters'

        if validation_errors:
            raise forms.ValidationError(validation_errors)

        return super().clean(*args, **kwargs)
