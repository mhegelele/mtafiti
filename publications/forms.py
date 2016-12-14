from dal import autocomplete
from djangoformsetjs.utils import formset_media_js
from django.forms import inlineformset_factory, ModelForm
from publications.models import Author, Publication, PublicationAuthor


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


class PublicationAuthorForm(ModelForm):
    class Meta:
        model = PublicationAuthor
        fields = '__all__'
        widgets = {
            'author': autocomplete.ModelSelect2(
                url='publications:author-autocomplete'
            )
        }


class PublicationForm(ModelForm):
    class Meta:
        model = Publication
        fields = '__all__'


PublicationAuthorFormset = inlineformset_factory(
    Publication,
    PublicationAuthor,
    form=PublicationAuthorForm
)
