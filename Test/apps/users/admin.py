from django.contrib import admin

from django.contrib.auth.models import User
from .models import Profile, Guild

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'rank')

	fields = [('user', 'slug'), ('money', 'reputation'), 'rank', 'status', 'bio']

@admin.register(Guild)
class GuildAdmin(admin.ModelAdmin):
	list_display = ('name', 'owner', 'verified')

	fields = [('name', 'owner'), 'members', 'verified']
	filter_horizontal = ['members']