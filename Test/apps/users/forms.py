from .models import Profile
from django import forms

class ProfileStatusForm(forms.ModelForm):
	fields = ['status',]
	class Meta:
		model = Profile
		exclude = ('user', 'bio', 'rank', 'money', 'reputation', 'slug')