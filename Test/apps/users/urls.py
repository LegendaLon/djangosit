from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
	path('profile/<int:pk>', views.ProfileView.as_view(), name="profile"),
	# path('profile/edit_status/<int:pk>', views.)
]