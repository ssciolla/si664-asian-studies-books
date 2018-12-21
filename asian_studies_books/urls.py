from django.urls import path, re_path
from . import views

# path('', views.index, name='index'),

urlpatterns = [
   path('', views.HomePageView.as_view(), name='home'),
   path('about/', views.AboutPageView.as_view(), name='about'),
   path('books/', views.BookListView.as_view(), name='books'),
   path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
   path('books/filter', views.BookFilterView.as_view(), kwargs=None, name='books_filter'),
   path('books/new/', views.BookCreateView.as_view(), name='book_new'),
   path('books/<int:pk>/delete', views.BookDeleteView.as_view(), name='book_delete'),
   path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book_update'),
]
