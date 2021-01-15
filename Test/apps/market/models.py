from django.db import models

from django.urls import reverse

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User

from django.utils.html import format_html

import string
import random

from django.utils import timezone
# Create your models here.

def generate_code(count=8):
	a = ""
	for _ in range(0, count):
		a += random.choice(string.ascii_lowercase)
	return a.upper()

class Category(models.Model):
	name = models.CharField("Название", blank=False, max_length = 60)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('market:category-detail', args = [self.id])

	class Meta:
		verbose_name = "Категорию"
		verbose_name_plural = "Категории"

class Companie(models.Model):
	name = models.CharField("Название", blank=False, max_length = 60)
	date_create = models.DateTimeField("Дата основания", default=timezone.now)
	owner = models.ForeignKey(
		User,
		blank = False,
		on_delete = models.CASCADE,
		related_name = "companie",
		verbose_name = "Владелец",
	)
	workers = models.ManyToManyField(User, verbose_name = "Работники", blank=True, related_name="workers")

	verified = models.BooleanField(
		default=False,
		verbose_name = "Доверенная компания",
	)

	def get_absolute_url(self):
		return reverse('market:companie-detail', args = [self.id])

	def __str__(self):
		return f"Компания: {self.name}"

	class Meta:
		verbose_name = "Компанию"
		verbose_name_plural = "Компании"

class Product(models.Model):
	title = models.CharField("Заголовок", blank = False, max_length = 100)
	description = models.TextField("Текст", blank=False)
	date = models.DateTimeField("Дата создания", default=timezone.now)
	category = models.ManyToManyField(Category, verbose_name = 'Категории товаров', blank=True, related_name="category")
	price = models.IntegerField(
		verbose_name = "Цена",
		blank = False,
	)
	availability = models.BooleanField(
		default=True,
		verbose_name = "В наличии",
	)
	provider = models.ForeignKey(
		Companie,
		blank = False,
		on_delete = models.CASCADE,
		related_name = "product",
		verbose_name = "Поставщик",
	)

	verified = models.BooleanField(
		default=False,
		verbose_name = "Одобренный",
	)

	# Ссылки на управление обьектом
	def get_update_url(self):
		return reverse("market:product-update", args = [self.id])

	def get_delete_url(self):
		return reverse("market:product-delete", args = [self.id])

	def get_absolute_url(self):
		return reverse("market:product-detail", args = [self.id])

	def was_availability(self):
		if self.availability:
			return "Есть в наличии"
		else:
			return "Нет в наличии"

	def __str__(self):
		return f"Заголовок: {self.title}, Компания: {self.provider.name}"

	class Meta:
		verbose_name = "Товар"
		verbose_name_plural = "Товары"

		ordering = ['-date',]

class PromoCode(models.Model):
	count = models.IntegerField(verbose_name = "Скидка", default = 0, blank = False, null = False)
	count_using = models.IntegerField(
		verbose_name = "Количество использованей",
		default = 1,
		blank = False,
	)
	creater = models.ForeignKey(
		User,
		blank = False,
		null = True,
		on_delete = models.CASCADE,
		related_name = "creater",
		verbose_name = "Создатель",
	)

	work_is = models.ManyToManyField(Product, verbose_name = 'Работают с', blank=True, related_name="work_is", help_text="Если оставите пустым, код не будет работать.")

	work_to = models.DateTimeField("Работает до", blank = True, null = True, help_text = "Оставьте пустым, чтоб код работал неограниченое кол. времяни.")
	date_create = models.DateTimeField("Дата создания промо акции", default=timezone.now, null = True)

	code = models.SlugField(blank=False, default=generate_code, null=True)

	def __str__(self):
		return f"{self.code} -- {str(self.count)}%"

	# Перегенирирует код
	def regenerate_code(self, count_len=8):
		self.code = generate_code(count_len)

	# Проверяет работает ли данная промо акция 
	def was_work(self):
		if self.work_to and timezone.now() <= self.work_to and self.count_using > 0:
			return True
		if not self.work_to and self.count_using > 0:
			return True
		else:
			return False

	def does_it_work(self):
		reason = ""
		if self.was_work():
			reason += "Работает. "
		else:
			reason += "Не работает. "

		if self.count_using <= 0:
			reason += "Количество использованей достигло 0. "
		if self.work_to and timezone.now() >= self.work_to:
			reason += "Закончилось время использования. "

		return reason

	class Meta:
		verbose_name = "Промо акцию"
		verbose_name_plural = "Промо акции"

class Order(models.Model):
	client = models.ForeignKey(
		User,
		blank = False,
		on_delete = models.CASCADE,
		related_name = "client",
		verbose_name = "Клиент",
	)
	product = models.ForeignKey(
		Product,
		blank = False,
		on_delete = models.CASCADE,
		related_name = "order",
		verbose_name = "Товар"
	)

	sale = models.ForeignKey(
		PromoCode,
		blank = True,
		null = True,
		on_delete = models.CASCADE,
		related_name = "sale",
		verbose_name = "Скидка",
	)

	status_choice = (
		("В ожидании", "В ожидании"),
		("Задерживаеться", "Задерживаеться"),
		("Принят", "Принят"),
		("Завершено", "Завершено"),
		("Отклонено", "Отклонено"),
	)
	status = models.CharField("Статус", choices=status_choice, default="В ожидании", blank=False, max_length = 60)
	count = models.IntegerField(verbose_name = "Количество", default = 1)
	date = models.DateTimeField("Дата оформления заказа", default=timezone.now)
	description = models.TextField("Описание к заказу", blank=True)	

	# Ссылки
	def get_absolute_url(self):
		return reverse("market:order-detail", args = [self.id])

	def get_update_url(self):
		return reverse("market:order-update", args = [self.id])

	def get_delete_url(self):
		return reverse("market:order-delete", args = [self.id])

	def was_price(self):
		if not self.sale:
			return ""
		else:
			return (self.product.price * self.count)

	def was_provider(self):
		return self.product.provider

	def was_total_price(self):
		if self.sale:
			return int((self.product.price * self.count) * (100 - self.sale.count) / 100)
		else:
			return (self.product.price * self.count)

	def __str__(self):
		return f"Номер заказа: {self.id}, Статус: {self.status}, Товар: {self.product.title}"

	class Meta:
		verbose_name = "Заказ"
		verbose_name_plural = "Заказы"
		ordering = ['-date',]

# @receiver(post_save, sender=Order)
# def save_user_profile(sender, instance, **kwargs):
# 	if instance.profile.slug != instance.username:
# 		instance.profile.slug = instance.username.lower()
# 	instance.profile.save()

""" Пример репорта """
# class Report(models.Model):
# 	user = models.ForeignKey(
# 		User,
# 		blank = False,
# 		on_delete = models.CASCADE,
# 		related_name = "user",
# 		verbose_name = "Пользователь",
# 	)
# 	evaluation = 