from django.views.generic.edit import CreateView
from .models import CommentInNews

class AuthorCreate(CreateView):
    model = CommentInNews
    fields = ['text', '']