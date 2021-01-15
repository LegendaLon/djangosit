from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, View
from django.views.generic import ListView, DetailView

from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

from .models import News, CommentInNews

from django.utils import timezone

# Create your views here.

class BasePageView(ListView):
	model = News
	template_name = "BasePage/index.html"

class NewsDetailView(DetailView):
	template_name = 'BasePage/detail.html'
	model = News

	def post(self, request, *args, **kwargs):
		news_id = request.path[-1]
		post = News.objects.get(id=news_id)
		if request.user:
			a = CommentInNews(text=request.POST['text'], author=request.user, news=post, date= timezone.now())
			a.save()
		return HttpResponseRedirect( reverse('basepage:detail', args = (news_id)))