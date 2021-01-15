from django.urls import path

from . import views

app_name = 'market'
urlpatterns = [
	# Товары
	path('product/', views.ProductListView.as_view(), name = "product-list"),
	path('product/<int:pk>', views.ProductDetailView.as_view(), name = "product-detail"),
	path('product/create/', views.ProductCreateView.as_view(), name = "product-create"),
	path('product/update/<int:pk>', views.ProductUpdateView.as_view(), name = "product-update"),
	path('product/delete/<int:pk>', views.ProductDeleteView.as_view(), name = "product-delete"),

	# Заказы
	path('order/', views.OrderListView.as_view(), name = "order-list"),
	path('order/client_list', views.OrderListClientView.as_view(), name = "order-clientlist"),
	path('order/<int:pk>', views.OrderDetailView.as_view(), name = "order-detail"),
	path('order/update/<int:pk>', views.OrderUpdateView.as_view(), name = "order-update"),
	path('order/delete/<int:pk>', views.OrderDeleteView.as_view(), name = "order-delete"),

	# Компании
	path('companie/', views.CompanieListView.as_view(), name = "companie-list"),
	path('companie/<int:pk>', views.CompanieDetailView.as_view(), name = "companie-detail"),

	# Категории
	path('category/<int:pk>', views.CategoryDetailView.as_view(), name = "category-detail"),
]