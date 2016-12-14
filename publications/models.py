from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import gettext_lazy as _
from django.core.urlresolvers import reverse
from publications.fields import PagesField


@python_2_unicode_compatible
class Author(models.Model):
    name = models.CharField(max_length=90, editable=False)
    first_name = models.CharField(_('First Name'), max_length=30)
    middle_name = models.CharField(_('Middle Name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=30)
    institution = models.CharField(_('Institution'), max_length=256, blank=True)
    email = models.EmailField(_('Email'), blank=True)

    def __str__(self):
        if not self.middle_name:
            return u'{} {}'.format(self.first_name, self.last_name)
        return u'{} {}. {}'.format(self.first_name, self.middle_name[0].upper(), self.last_name)

    def get_absolute_url(self):
        return reverse('publications:edit-author', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        if self.id is None and self.name:
            names = [name for name in self.name.split(' ')]
            if len(names) > 2:
                self.first_name = names[0]
                self.middle_name = names[1]
                self.last_name = names[2]
            elif 1 < len(names) < 3:
                self.first_name = names[0]
                self.last_name = names[1]
        elif self.id is None and not self.name:
            if not self.middle_name:
                self.name = '{} {}'.format(self.first_name, self.last_name)
            else:
                self.name = '{} {} {}'.format(self.first_name, self.middle_name, self.last_name)
        super(Author, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Publication(models.Model):
    class Meta:
        ordering = ['-year', '-id']
        verbose_name_plural = 'Publications'

    title = models.CharField(_('Title'), max_length=512, unique=True)
    authors = models.ManyToManyField(Author, through='PublicationAuthor', editable=False)
    keywords = models.CharField(_('Research Area'), max_length=512)
    year = models.PositiveIntegerField(_('Year'))
    journal = models.CharField(_('Journal'), max_length=256, blank=True)
    volume = models.IntegerField(_('Volume'), blank=True, null=True)
    number = models.IntegerField(blank=True, null=True, verbose_name=_('Issue'))
    pages = PagesField(max_length=32, blank=True)
    doi = models.CharField(max_length=128, verbose_name=_('DOI'), blank=True)
    confirmed = models.BooleanField(default=False, editable=False)
    created = models.DateTimeField(_('Date Added'), auto_now_add=True)
    updated = models.DateTimeField(_('Last Updated'), auto_now=True)

    def __init__(self, *args, **kwargs):
        models.Model.__init__(self, *args, **kwargs)

        # post-process keywords
        self.keywords = self.keywords.replace(';', ',')
        self.keywords = self.keywords.replace(', and ', ', ')
        self.keywords = self.keywords.replace(',and ', ', ')
        self.keywords = self.keywords.replace(' and ', ', ')
        self.keywords = [s.strip().lower() for s in self.keywords.split(',')]
        self.keywords = ', '.join(self.keywords).lower()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('publications:edit-publication', kwargs={'pk': self.id})

    def _get_publication_url(self):
        """Returns the publication's URL by building it from doi field."""
        if self.doi:
            return 'https://doi.org/{}'.format(self.doi)
        else:
            return None
    url = property(_get_publication_url)

    def _get_keywords(self):
        if self.keywords:
            return [keyword.strip().lower() for keyword in self.keywords.split(',')]
        return None
    research_area = property(_get_keywords)


class PublicationAuthor(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, models.CASCADE)
    first_author = models.BooleanField(_('First Author?'), default=False)
    corresponding_author = models.BooleanField(_('Corresponding Author?'), default=False)
