# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse

class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'country'
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.country_name


class Creator(models.Model):
    creator_id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=45)
    first_name = models.CharField(max_length=45)
    display_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'creator'
        verbose_name = 'Creator'
        verbose_name_plural = 'Creators'

    def __str__(self):
        return self.display_name


class Format(models.Model):
    format_id = models.AutoField(primary_key=True)
    format_code = models.CharField(unique=True, max_length=10)
    format_name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'format'
        verbose_name = 'Format'
        verbose_name_plural = 'Formats'

    def __str__(self):
        return self.format_name


class Institution(models.Model):
    institution_id = models.AutoField(primary_key=True)
    institution_name = models.CharField(max_length=200)
    oclc_symbol = models.CharField(max_length=5)
    street_address = models.CharField(max_length=300, blank=True, null=True)
    country = models.ForeignKey(Country, models.CASCADE)
    opac_url = models.CharField(max_length=700, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'institution'
        verbose_name = 'Institution'
        verbose_name_plural = 'Institutions'

    def __str__(self):
        return self.institution_name


class Publisher(models.Model):
    publisher_id = models.AutoField(primary_key=True)
    publisher_name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'publisher'
        verbose_name = 'Publisher'
        verbose_name_plural = 'Publishers'

    def __str__(self):
        return self.publisher_name


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'role'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.role_name


class Series(models.Model):
    series_id = models.AutoField(primary_key=True)
    series_name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'series'
        verbose_name = 'Series'
        verbose_name_plural = 'Series'

    def __str__(self):
        return self.series_name


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    prefix = models.CharField(max_length=100, blank=True, null=True)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    full_title = models.CharField(max_length=300, blank=True, null=True)
    key_note = models.CharField(max_length=400, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    pages = models.IntegerField(blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)
    publisher = models.ForeignKey('Publisher', models.CASCADE)
    series = models.ForeignKey('Series', models.CASCADE, blank=True, null=True)

    creators = models.ManyToManyField(Creator, through='Attribution')
    institutions = models.ManyToManyField(Institution, through='Holding')

    class Meta:
        managed = False
        db_table = 'book'
        verbose_name = 'Asian Studies Book'
        verbose_name_plural = 'Asian Studies Books'

    def __str__(self):
        return self.full_title

    def display_creators(self):
        """Create a string for creators. This is required to display in the Admin view."""
        attributions = self.attributions.select_related('creator', 'book', 'role')
        attribution_strings = []
        for attribution in attributions:
            attribution_string = ''
            attribution_string += attribution.creator.display_name
            if attribution.role != None:
                attribution_string += " ({})".format(attribution.role)
            attribution_strings.append(attribution_string)
        return ', '.join(attribution_strings)

    def display_versions(self):
        versions = self.versions.all()
        version_strings = []
        for version in versions:
            version_string = ''
            version_string += str(version.format)
            if version.year_published != None:
                version_string += " - " + str(version.year_published)
            if version.isbn13 != None:
                version_string += " - " + str(version.isbn13)
            if version.bisac_status != None:
                version_string += " - " + str(version.bisac_status)
            version_strings.append(version_string)
        return version_strings

    # Choosing not to create an equivalent method for institutions (there are too many!)

    # def get_absolute_url(self):
    #     return reverse('site_detail', kwargs={'pk': self.pk})


class Holding(models.Model):
    holding_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, models.CASCADE)
    institution = models.ForeignKey('Institution', models.CASCADE)

    class Meta:
        managed = False
        db_table = 'holding'
        verbose_name = 'Holding'
        verbose_name_plural = 'Holding'


class Attribution(models.Model):
    attribution_id = models.AutoField(primary_key=True)
    book = models.ForeignKey('Book', models.CASCADE, related_name='attributions')
    creator = models.ForeignKey('Creator', models.CASCADE)
    role = models.ForeignKey('Role', models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'attribution'
        verbose_name = 'Attribution'
        verbose_name_plural = 'Attributions'


class Version(models.Model):
    version_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, models.CASCADE, related_name='versions')
    format = models.ForeignKey(Format, models.CASCADE)
    isbn13 = models.CharField(max_length=13, blank=True, null=True)
    year_published = models.IntegerField(blank=True, null=True)
    bisac_status = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'version'
        verbose_name = 'Version'
        verbose_name_plural = 'Versions'
