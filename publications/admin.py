from django.contrib import admin

from publications.models import Author, Publication, PublicationAuthor
from publications.forms import PublicationAuthorForm


class PublicationAuthorAdmin(admin.TabularInline):
    model = PublicationAuthor
    form = PublicationAuthorForm
    extra = 1


class PublicationAdmin(admin.ModelAdmin):
    list_display = ['title', 'journal', 'year']
    fieldsets = [
        (None, {'fields': ('title', 'research_area', 'journal', 'year', 'volume', 'number', 'pages', 'doi')})
    ]
    inlines = [PublicationAuthorAdmin]

admin.site.register(Publication, PublicationAdmin)
admin.site.register(Author)
