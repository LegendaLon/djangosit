from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class News(models.Model):
	title = models.CharField("Заголовок", max_length = 50)
	text = models.TextField("Текст")
	author = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
	)
	date = models.DateTimeField("Дата создания", default=timezone.now)
	archived = models.BooleanField(default=False)

	def __str__(self):
		return f"Заголовок: {self.title} пользователь: {self.author} "

	class Meta:
		verbose_name = "Новость"
		verbose_name_plural = "Новости"
		ordering = ['-date']

class CommentInNews(models.Model):
	text = models.TextField("Текст")
	author = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
	)
	news = models.ForeignKey(
		News,
		on_delete=models.CASCADE,
		related_name='comment',
	)
	date = models.DateTimeField("Дата создания", default=timezone.now)

	def __str__(self):
		return self.news.title

	def was_user_in_author(self, user):
		return self.author == user

	class Meta:
		verbose_name = "Коментарий"
		verbose_name_plural = "Коментарии"
		ordering = ['-date']