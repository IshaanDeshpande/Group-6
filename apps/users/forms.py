from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-input text-right', 'placeholder': 'Username'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-input text-right', 'placeholder': 'Email'}),
    )
    zip_code = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-input text-right', 'placeholder': 'Zip Code'}),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input text-right', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input text-right', 'placeholder': 'Re-Enter Password'}),
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data


class ProfileForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-input'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-input'}),
    )
    zip_code = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input'}),
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Leave blank to keep current password'}),
    )

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        if self.user and User.objects.exclude(pk=self.user.pk).filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input text-center text-xl md:text-2xl lg:text-3xl py-6 md:py-8 lg:py-10',
            'placeholder': 'Username / Email',
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input text-center text-xl md:text-2xl lg:text-3xl py-6 md:py-8 lg:py-10',
            'placeholder': 'Password',
        }),
    )
