# forms.py
from django import forms
from .models import Product, Order, Category

from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
	fields = ['title', 'description', 'category', 'price']
	class Meta:
		model = Product
		exclude = ('provider', 'date', 'availability', 'verified')

	# category = forms.ModelMultipleChoiceField(
	# 	queryset=Category.objects.all(),
	# 	widget=forms.CheckboxSelectMultiple
	# )

class OrderForm(forms.ModelForm):
	fields = ['count', 'description']
	class Meta:
		model = Order
		exclude = ('client', 'product', 'status', 'date', 'sale')
