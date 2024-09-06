from django import forms
from django.contrib.auth.models import User
from .models import Profile, Review


# class PurchaseForm(forms.Form):
#     quantity = forms.IntegerField(min_value=1, widget=forms.HiddenInput())
#
#     def __init__(self, *args, **kwargs):
#         self.stock = kwargs.pop('stock', None)
#         super().__init__(*args, **kwargs)
#         if self.stock:
#             self.fields['quantity'].widget.attrs.update({
#                 'min': self.stock.minimum_purchase_quantity,
#                 'max': self.stock.remaining_quantity,
#                 'data-price-per-unit': self.stock.price_per_unit
#             })


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
