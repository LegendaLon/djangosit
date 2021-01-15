from django.shortcuts import render

from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView 

from django.http import HttpResponseRedirect

from .models import Category, Companie, Product, Order, PromoCode

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from .forms import ProductForm, OrderForm

from django.contrib import messages

def get_user_companie(user):
	companie = None
	if user.is_authenticated:
		try:
			companie = Companie.objects.all().filter(owner=user)
		except:
			companie = Companie.objects.all().filter(workers=user)	
	return companie

# Create your views here.

""" Продукты """
# Список продуктов
class ProductListView(ListView):
	model = Product
	template_name = "market/product/product_list.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['companie_owner'] = get_user_companie(self.request.user)
		return context

# Показывает данные о товаре, на странице есть форма для оставление заказа
class ProductDetailView(DetailView, CreateView):
	model = Product
	template_name = "market/product/product_detail.html"
	form_class = OrderForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['companie_owner'] = get_user_companie(self.request.user)
		return context

	# Оставляет заказ
	def form_valid(self, form):
		product = Product.objects.get(id=self.request.path.split("/")[-1])

		if product.verified:
			messages.success(self.request, "Заказ успешно оформлен.")
			messages.success(self.request, "Ожидайте пока содрудки компании примут Ваш заказ.")
			if self.request.POST['sale'] != "":
				code = PromoCode.objects.get(code = self.request.POST['sale'])
				if code.was_work() and code and product in code.work_is.all():
					form.instance.sale = code
					code.count_using -= 1
					code.save()

					messages.success(self.request, f"Вы использовали код '{code.code}' который дает {code.count}% скидки.")
			form.instance.client = self.request.user
			form.instance.product = product
			form.instance.status = "В ожидании"
			form.instance.date = timezone.now()
			return super(ProductDetailView, self).form_valid(form)
		else:
			messages.error(self.request, "Заказ не оформлен.")
			messages.error(self.request, "Продукт не был проверен модераторами.")
			return HttpResponseRedirect(reverse('market:product-detail', args = [product.id]))

# Создание продукта
class ProductCreateView(CreateView):
	model = Product
	form_class = ProductForm
	template_name = "market/product/product_create.html"

	# 
	def form_valid(self, form):
		companie = get_user_companie(self.request.user)[0]
		form.instance.provider = companie
		form.instance.date = timezone.now()
		form.instance.availability = True
		if companie.verified:
			form.instance.verified = True
		else:
			form.instance.verified = False

		messages.success(self.request, "Товар успешно добавлен")
		return super(ProductCreateView, self).form_valid(form)

# Редактирование продука
class ProductUpdateView(UpdateView):
	model = Product
	template_name = "market/product/product_update.html"
	fields = ['title', 'description', 'category', 'price', 'availability']

# Удаление продукта
class ProductDeleteView(DeleteView):
	model = Product
	template_name = "market/product/product_update.html"
	success_url = reverse_lazy('market:product-list')

""" Заказы """
# Список заказов для сотрудников
class OrderListView(ListView):
	model = Order
	template_name = "market/order/order_list.html"

# Список заказов для клиента
class OrderListClientView(ListView):
	model = Order
	template_name = "market/order/order_list_client.html"

# Показывает детали заказа
class OrderDetailView(DetailView):
	model = Order
	template_name = "market/order/order_detail.html"

# Возможность изменить статус для персонала
class OrderUpdateView(UpdateView):
	model = Order
	template_name = "market/order/order_update.html"
	fields = ['status']

# Удаление заказа
class OrderDeleteView(DeleteView):
	model = Order
	template_name = "market/order/order_delete.html"
	success_url = reverse_lazy('market:order-list')

""" Компании """
# Список компаний
class CompanieListView(ListView):
	model = Companie
	template_name = "market/companie/companie_list.html"

# Детили компании
class CompanieDetailView(DetailView):
	model = Companie
	template_name = "market/companie/companie_detail.html"

""" Категории """
# Список категорий
class CategoryListView(ListView):
	model = Category
	template_name = ""

# Детали категорий
class CategoryDetailView(DetailView):
	model = Category
	template_name = "market/category/category_detail.html"