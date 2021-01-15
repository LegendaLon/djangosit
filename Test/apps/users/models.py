from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from django.urls import reverse
from django.utils import timezone
# Профиль
class Guild(models.Model):
	name = models.CharField("Название", blank=False, max_length = 60)
	date_create = models.DateTimeField("Дата основания", default=timezone.now)
	owner = models.ForeignKey(
		User,
		blank = False,
		on_delete = models.CASCADE,
		related_name = "guild",
		verbose_name = "Владелец",
	)
	members = models.ManyToManyField(User, verbose_name = "Участики", blank=True, related_name="members")

	verified = models.BooleanField(
		default=False,
		verbose_name = "Доверенный клан",
	)

	def __str__(self):
		return f"{self.name}"

	class Meta:
		verbose_name = "Клан"
		verbose_name_plural = "Кланы"
		
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name = "Пользователь")
	bio = models.TextField(verbose_name = "Информация", max_length=500, blank=True)
	status = models.CharField("Статус", blank=True, max_length = 50)
	rank = models.CharField("Ранг", default = "Пользователь", blank = False, max_length = 50)

	money = models.IntegerField(verbose_name = "Деньги", default = 0)
	reputation = models.IntegerField(verbose_name = "Репутация", default = 0)

	slug = models.SlugField(blank=False)

	def __str__(self):
		return f"Профиль {self.user.username}"

	# Получение ссылок
	def get_absolute_url(self):
		return reverse('users:profile', args = [self.user.id])

	class Meta:
		verbose_name = "Профиль"
		verbose_name_plural = "Профили"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance, slug=instance.username.lower())

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	if instance.profile.slug != instance.username:
		instance.profile.slug = instance.username.lower()
	instance.profile.save()