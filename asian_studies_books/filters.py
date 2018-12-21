import django_filters
from asian_studies_books.models import Book, Creator, Attribution, Publisher, Series, Version, Format


class BookFilter(django_filters.FilterSet):
	full_title = django_filters.CharFilter(
		field_name='full_title',
		label='Book Title',
		lookup_expr='icontains'
	)

	creators = django_filters.CharFilter(
		field_name='attributions__creator__display_name',
		label='Creator(s)',
		lookup_expr='icontains'
	)

	description = django_filters.CharFilter(
		field_name='description',
		label='Description',
		lookup_expr='icontains'
	)

	publisher = django_filters.ModelChoiceFilter(
		field_name='publisher__publisher_name',
		label='Publisher',
		queryset=Publisher.objects.all().order_by('publisher_name'),
		lookup_expr='exact'
	)

	series = django_filters.ModelChoiceFilter(
		field_name='series__series_name',
		label='Series',
		queryset=Series.objects.all().order_by('series_name'),
		lookup_expr='exact'
	)

	format = django_filters.ModelChoiceFilter(
		field_name='versions__format__format_name',
		label='Format',
		queryset=Format.objects.all().order_by('format_name'),
		lookup_expr='exact'
	)

	class Meta:
		model = Book
		# form = SearchForm
		# fields [] is required, even if empty.
		fields = []
