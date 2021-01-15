from django.urls import path

from . import views

app_name = 'basepage'
urlpatterns = [
    path('', views.BasePageView.as_view(), name = 'index'),
    path('news/<int:pk>', views.NewsDetailView.as_view(), name = 'detail'),
]