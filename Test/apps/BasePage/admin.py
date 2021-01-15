from django.contrib import admin

from .models import News, CommentInNews

# Register your models here.

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'date', 'archived')
	list_filter = ('date', 'archived')

	fields = ['title', 'text', 'author', 'date']
@admin.register(CommentInNews)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('author', 'news',  'text', 'date')
	list_filter = ('date',)

	fields = ['text', 'author', 'news', 'date']