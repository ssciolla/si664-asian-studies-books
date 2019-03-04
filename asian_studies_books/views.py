from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.db.models import F, Q

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_filters.views import FilterView

from .forms import BookForm
from .models import Book, Creator, Attribution, Holding, Institution
from .filters import BookFilter

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

## I tried to implement this, but when I did, my filter fields disappeared on the sidebar.
## I could not figure out why, so I moved on.

# # Taken from Anthony Whyte's heritagesites/views.py:
# # https://github.com/UMSI-SI664-2018Fall/heritagesites/blob/master/heritagesites/views.py

# class PaginatedFilterView(generic.View):
#     """
#     Creates a view mixin, which separates out defaut 'page' keyword and returns the
#     remaining quertystring as a new template context variable.
#     https://stackoverflow.com/questions/51389848/how-can-i-use-pagination-with-django-filter
#     """
#     def get_context_data(self, **kwargs):
#         context = super(PaginatedFilterView, self).get_context_data(**kwargs)
#         if self.request.GET:
#             querystring = self.request.GET.copy()
#             if self.request.GET.get('page'):
#                 del querystring['page']
#             context['querystring'] = quertystring.urlencode()
#             return context

class BookFilterView(FilterView):
    filterset_class = BookFilter
    template_name = 'asian_studies_books/book_filter.html'
    # paginate_by = 30

@method_decorator(login_required, name='dispatch')
class BookCreateView(generic.View):
    model = Book
    form_class = BookForm
    success_message = "Book created successfully"
    template_name = 'asian_studies_books/book_new.html'
    # fields = '__all__' <-- superseded by form_class

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        form = BookForm(request.POST)
        if form.is_valid():
            book_new = form.save(commit=False)
            book_new.save()
            for creator_name in form.cleaned_data['creators']:
                Attribution.objects.create(book=book_new, creator=creator_name)
            # return redirect(site) # shortcut to object's get_absolute_url()
            return HttpResponseRedirect(book_new.get_absolute_url())
        return render(request, 'asian_studies_books/book_new.html', {'form': form})

    def get(self, request):
        form = BookForm()
        return render(request, 'asian_studies_books/book_new.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class BookUpdateView(generic.UpdateView):
    model = Book
    form_class = BookForm
    # fields = '__all__' <-- superseded by form_class
    context_object_name = 'book'
    # pk_url_kwarg = 'site_pk'
    success_message = "Book updated successfully"
    template_name = 'asian_studies_books/book_update.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        book = form.save(commit=False)
        # site.updated_by = self.request.user
        # site.date_updated = timezone.now()
        book.save()

        # Current creator_id values linked to site
        old_ids = Attribution.objects\
                    .values_list('creator_id', flat=True)\
                    .filter(book_id=book.book_id)

        # New countries list
        new_creators = form.cleaned_data['creators']

        new_ids = []

        # Insert new unmatched creator entries
        for creator in new_creators:
            new_id = creator.creator_id
            new_ids.append(new_id)
            if new_id in old_ids:
                continue
            else:
                Attribution.objects\
                    .create(book=book, creator=creator)

        # Delete old unmatched country entries
        for old_id in old_ids:
            if old_id in new_ids:
                continue
            else:
                Attribution.objects\
                    .filter(book_id=book.book_id, creator_id=old_id)\
                    .delete()

        return HttpResponseRedirect(book.get_absolute_url())
        # return redirect('heritagesites/site_detail', pk=site.pk)

@method_decorator(login_required, name='dispatch')
class BookDeleteView(generic.DeleteView):
    model = Book
    success_message = "Book deleted successfully"
    success_url = reverse_lazy('books')
    context_object_name = 'book'
    template_name = 'asian_studies_books/book_delete.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Delete Attribution entries
        Attribution.objects\
            .filter(book_id=self.object.book_id)\
            .delete()

        self.object.delete()

        return HttpResponseRedirect(self.get_success_url())
