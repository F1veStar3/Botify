from django import forms
from django.contrib.auth.models import User
from .models import Profile, Review, Notification


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'message']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'email', 'subject', 'message']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['logo']
