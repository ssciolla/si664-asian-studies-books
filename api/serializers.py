from asian_studies_books.models import Book, Creator, Country, Format, Institution, Publisher, Role, Series, Holding, Attribution, Version
from rest_framework import response, serializers, status


class CountrySerializer(serializers.ModelSerializer):

	class Meta:
		model = Country
		fields = ('country_id', 'country_name')


class FormatSerializer(serializers.ModelSerializer):

	class Meta:
		model = Format
		fields = ('format_id', 'format_code', 'format_name')


class PublisherSerializer(serializers.ModelSerializer):

	class Meta:
		model = Publisher
		fields = ('publisher_id', 'publisher_name')

class RoleSerializer(serializers.ModelSerializer):

	class Meta:
		model = Role
		fields = ('role_id', 'role_name')

class SeriesSerializer(serializers.ModelSerializer):

	class Meta:
		model = Series
		fields = ('series_id', 'series_name')

class InstitutionSerializer(serializers.ModelSerializer):
	country = CountrySerializer(many=False, read_only=True)

	class Meta:
		model = Institution
		fields = (
			'institution_id',
			'institution_name',
			'oclc_symbol',
			'street_address',
			'country',
			'opac_url')

class BookSerializer(serializers.ModelSerializer):
	publisher = PublisherSerializer(many=False, read_only=True)
	series = SeriesSerializer(many=False, read_only=True)

	class Meta:
		model = Book
		fields = (
			'book_id',
			'title',
			'prefix',
			'subtitle',
			'full_title',
			'key_note',
			'description',
			'pages',
			'volume',
			'publisher',
			'series')
			# 'creators', # not sure about these
			# 'institutions')

class VersionSerializer(serializers.ModelSerializer):
	book = BookSerializer(many=False, read_only=True)
	format = FormatSerializer(many=False, read_only=True)

	class Meta:
		model = Version
		fields = (
			'version_id',
			'book',
			'format',
			'isbn13',
			'year_published',
			'biasc_status')


class AttributionSerializer(serializers.ModelSerializer):
	book_id = serializers.ReadOnlyField(source='book.book_id')
	creator_id = serializers.ReadOnlyField(source='creator.creator_id')
	role = RoleSerializer(many=False, read_only=True)

	class Meta:
		model = Attribution
		fields = ('book_id', 'creator_id', 'role')

class HoldingSerializer(serializers.ModelSerializer):
	book_id = serializers.ReadOnlyField(source='book.book_id')
	institution_id = serializers.ReadOnlyField(source='institution.institution_id')

	class Meta:
		model = Holding
		fields = ('book_id', 'institution_id')


class CreatorSerializer(serializers.ModelSerializer):
	last_name = serializers.CharField(
		allow_blank=False,
		max_length=45
	)
	first_name = serializers.CharField(
		allow_blank=False
	)
	display_name = serializers.CharField(
		allow_blank=True,
		max_length=100
	)
	attribution = AttributionSerializer(
		source='attribution_set', # Note use of _set
		many=True,
		read_only=True
	)
	attribution_ids = serializers.PrimaryKeyRelatedField(
		many=True,
		write_only=True,
		queryset=Book.objects.all(),
		source='attribution'
	)

	class Meta:
		model = Creator
		fields = (
			'last_name',
			'first_name',
			'display_name',
			'attribution',
			'attribution_ids'
		)

	def create(self, validated_data):
		"""
		This method persists a new HeritageSite instance as well as adds all related
		countries/areas to the heritage_site_jurisdiction table.  It does so by first
		removing (validated_data.pop('heritage_site_jurisdiction')) from the validated
		data before the new HeritageSite instance is saved to the database. It then loops
		over the heritage_site_jurisdiction array in order to extract each country_area_id
		element and add entries to junction/associative heritage_site_jurisdiction table.
		:param validated_data:
		:return: site
		"""

		# print(validated_data)

		books = validated_data.pop('attribution')
		creator = Creator.objects.create(**validated_data)

		if books is not None:
			for book in books:
				Attribution.objects.create(
					creator_id=creator.creator_id,
					book_id=book.book_id,
					role_id=None # Not worrying about this right now, may return to it later.
				)
		return creator

	def update(self, instance, validated_data):
		creator_id = instance.creator_id
		new_books = validated_data.pop('attribution')

		instance.last_name = validated_data.get(
			'last_name',
			instance.last_name
		)
		instance.first_name = validated_data.get(
			'first_name',
			instance.first_name
		)
		instance.display_name = validated_data.get(
			'display_name',
			instance.display_name
		)
		instance.save()

		# If any existing books are not in updated list, delete them
		new_ids = []
		old_ids = Attribution.objects \
			.values_list('book_id', flat=True) \
			.filter(creator_id__exact=creator_id)

		# TODO Insert may not be required (Just return instance)

		# Insert new unmatched book entries
		for book in new_books:
			new_id = book.book_id
			new_ids.append(new_id)
			if new_id in old_ids:
				continue
			else:
				Attribution.objects \
					.create(creator_id=creator_id, book_id=new_id, role_id=None)

		# Delete old unmatched book entries
		for old_id in old_ids:
			if old_id in new_ids:
				continue
			else:
				Attribution.objects \
					.filter(creator_id=creator_id, book_id=old_id) \
					.delete()

		return instance
