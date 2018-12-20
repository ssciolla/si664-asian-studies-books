from django.contrib import admin

# Register your models here.
import asian_studies_books.models as models

@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
	fields = [
		'country_name'
	]

	list_display = [
		'country_name'
	]

# admin.site.register(models.CountryArea)

@admin.register(models.Creator)
class CreatorAdmin(admin.ModelAdmin):
	fields = ['last_name', 'first_name', 'display_name']
	list_display = ['last_name', 'first_name', 'display_name']

# admin.site.register(models.DevStatus)

@admin.register(models.Format)
class FormatAdmin(admin.ModelAdmin):
	fields = ['format_code', 'format_name']
	list_display = ['format_code', 'format_name']

# admin.site.register(models.HeritageSite)


@admin.register(models.Institution)
class InstitutionAdmin(admin.ModelAdmin):
	fields = ['institution_name', 'oclc_symbol', 'street_address', 'country', 'opac_url']
	list_display = ['institution_name', 'oclc_symbol', 'street_address', 'country', 'opac_url']


@admin.register(models.Publisher)
class PublisherAdmin(admin.ModelAdmin):
    fields = ['publisher_name']
    list_display = ['publisher_name']


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    fields = ['role_name']
    list_display = ['role_name']


@admin.register(models.Series)
class SeriesAdmin(admin.ModelAdmin):
	fields = ['series_name']
	list_display = ['series_name']


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
	fields = [
		'title',
	 	'prefix',
		'subtitle',
		'full_title',
		'key_note',
		'description',
		'pages',
		'volume',
		'publisher',
		'series'
	  	'display_creators'
	]
	list_display = [
		'title',
 		  'prefix',
		  'subtitle',
		  'full_title',
		  'key_note',
		  'description',
		  'pages',
		  'volume',
		  'publisher',
		  'series',
		  'display_creators'
	]
