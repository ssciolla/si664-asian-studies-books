from django.shortcuts import render
from django.views import generic

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Book, Creator, Attribution, Holding, Institution
from django.db.models import F, Q

# Create your views here.

class AboutPageView(generic.TemplateView):
    template_name = 'asian_studies_books/about.html'

class HomePageView(generic.TemplateView):
    template_name = 'asian_studies_books/home.html'

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'asian_studies_books/books.html'
    paginate_by = 50

    def get_queryset(self):
        books = Book.objects.all().select_related('publisher', 'series').order_by('title')
        return books

class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'asian_studies_books/book_detail.html'
