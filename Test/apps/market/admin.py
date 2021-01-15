from django.contrib import admin

from .models import Category, Companie, Product, Order, PromoCode

from .models import generate_code

from django.urls import reverse, path
from django.utils.html import format_html

from django.contrib import messages

from django.http import HttpResponseRedirect

# Register your models here.
# 
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['id', 'name']
	list_display_links = ['name',]

# 
class OrderInProductAdmin(admin.StackedInline):
	model = Order
 
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ['id', 'title', 'price', 'availability', 'verified', 'provider', "date"]
	list_display_links = ['title',]

	list_filter = ['availability', 'verified', 'date']

	search_fields = ['^title', '^price']

	inlines = (OrderInProductAdmin,)
	filter_horizontal = ['category']

	fields = [('title', 'provider'), 'description', 'price', 'category', 'verified']
# 
@admin.register(Companie)
class CompanieAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'date_create', 'owner']
	list_display_links = ['name',]

	list_filter = ['date_create', 'verified']


	filter_horizontal = ['workers']

	fields = ['name', 'owner', 'workers', 'verified']
# 
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ['id','product', 'client', 'was_provider', 'status', "count", "date", 'was_price', 'was_total_price']
	list_display_links = ['product']

	list_filter = ['status', 'date',]

	ordering = ['-date',]

	# fieldsets = (
	# 	(None, {
	# 		'fields': ('code', 'creater'),
	# 	}),
	# 	("Настройка", {
	# 		'fields': ('count', 'count_using', 'work_is'),
	# 		'classes': ('grp-collapse grp-open',),
	# 	}),
	# 	('Даты', {
	# 		'fields': ('work_to', 'date_create'),
	# 		'classes': ('grp-collapse grp-open',),
	# 	}),
	# )

	radio_fields = {"status": admin.HORIZONTAL}
	fields = [('product', 'client'), 'count', 'status', "description", 'sale']
# 
@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
	list_display = ['id', 'code', 'count_using', 'count', 'creater', 'code_status', 'code_actions']
	list_display_links = ['code',]

	list_filter = ['count', 'work_to']

	readonly_fields = ['code_actions', 'code_status']

	filter_horizontal = ['work_is']

	fieldsets = (
		("Главная", {
			'fields': ('code_status', 'code', 'code_actions'),
		}),
		("Настройка", {
			'fields': ('count', 'count_using', 'creater', 'work_is'),
			'classes': ('grp-collapse grp-open',),
		}),
		('Даты', {
			'fields': ('work_to', 'date_create'),
			'classes': ('grp-collapse grp-open',),
		}),
	)

	def get_urls(self):
		urls = super().get_urls()
		custom_urls = [
			path('<code_id>/regenerate/', self.admin_site.admin_view(self.regenerate_action), name='market_promocode_regenerate'),
		]
		return custom_urls + urls

	def code_actions(self, obj):
		regenerate_url = reverse('admin:market_promocode_regenerate', args = [obj.pk,])
		return format_html(
			f'<a class="button" href="{regenerate_url}">Перегенерировать код</a>'
		)

	def code_status(self, obj):
		return obj.does_it_work()

	code_actions.short_description = 'Действия'
	code_actions.allow_tags = True
	# code_actions.help_text = "Не нажимайте эту кнопку если обьект не создан"

	code_status.short_description = "Статус"
	code_status.allow_tags = True

	def regenerate_action(self, request, code_id, *args, **kwargs):
		if code_id != "None":
			obj = PromoCode.objects.get(id=code_id)

			obj.regenerate_code()
			obj.count_using = 10
			obj.work_to = None
			obj.save()
			messages.success(request, "Код перегенерирован, выдано 10 использованей и убрано ограничение по времяни использования.")
			return HttpResponseRedirect(reverse('admin:market_promocode_changelist', current_app=self.admin_site.name))
		else:
			messages.error(request, f"Вы не можете применить данную функцию к несуществующему обьекту.")
			return HttpResponseRedirect(reverse('admin:market_promocode_add', current_app=self.admin_site.name))