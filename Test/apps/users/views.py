from django.shortcuts import render
from django.views.generic import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView 

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileStatusForm

# Create your views here.

class ProfileView(DetailView):
	model = User
	template_name = "users/profile.html"

	def get(self, request, **kwargs):
		user = User.objects.get(id=request.path.split("/")[-1])
		return render(
			request,
			self.template_name,
			{"users":user})

	def post(self, request, **kwargs):
		profile = Profile.objects.get(id=request.path.split("/")[-1])
		if request.user == profile.user:
			profile.bio = request.POST["bio"]
			profile.status = request.POST["status"]
			profile.save()
			messages.success(request, "Изменения успешно внесены")
		return HttpResponseRedirect(reverse('users:profile', args = [request.path.split("/")[-1]]))
	# def get(self, request, pk):
	# 	# profile = Profile.objects.get(slug=slug)
	# 	# user = profile.user
	# 	user = User.objects.get(id=pk)
	# 	return render(
	# 		request,
	# 		self.template_name,
	# 		{"object":user}
	# 		)