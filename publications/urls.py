from django.conf.urls import url
from publications import views

app_name = 'publications'
urlpatterns = [
    url(r'^author-autocomplete/$', views.AuthorAutocomplete.as_view(create_field='name'), name='author-autocomplete'),
    url(r'^$', views.publication_listing, name='publication-listing'),
    url(r'^publication/add/$', views.manage_publication, name='add-publication'),
    url(r'^publication/(?P<pk>[0-9]+)/$', views.publication_details, name='publication-details'),
    url(r'^publication/(?P<pk>[0-9]+)/edit/$', views.manage_publication, name='edit-publication'),
    url(r'^publication/confirm-publication-details/$', views.confirm_publication_details,
        name='confirm-publication-details'),
    url(r'^author/add/$', views.manage_author, name='add-author'),
    url(r'^author/(?P<pk>[0-9]+)/$', views.author_detail, name='author-details'),
    url(r'^author/(?P<pk>[0-9]+)/edit/$', views.manage_author, name='edit-author'),
]
