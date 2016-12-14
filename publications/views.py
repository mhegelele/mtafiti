import json
from dal import autocomplete
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django.shortcuts import get_object_or_404, redirect, render
from .models import Author, Publication
from .forms import AuthorForm, PublicationForm, PublicationAuthorFormset


class AuthorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Author.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


@login_required
def publication_listing(request):
    publication_list = Publication.objects.all().order_by('-year', '-id')
    paginator = Paginator(publication_list, 10)

    page = request.GET.get('page')
    try:
        publications = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        publications = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        publications = paginator.page(paginator.num_pages)
    return render(request, 'publications/publication_listing.html', {'publications': publications})


@login_required
def manage_publication(request, pk=None):
    if pk:
        publication = get_object_or_404(Publication, pk=pk)
        action = reverse('publications:edit-publication', kwargs={'pk': pk})
    else:
        publication = Publication()
        action = reverse('publications:add-publication')
    form = PublicationForm(request.POST or None, instance=publication)
    formset = PublicationAuthorFormset(request.POST or None, request.FILES or None, instance=publication)
    if form.is_valid() and formset.is_valid():
        publication = form.save()
        publication_authors = formset.save(commit=False)
        for instance in publication_authors:
            instance.publication = publication
            instance.save()
        return redirect(reverse('publications:publication-details', kwargs={'pk': publication.pk}))
    return render(
        request,
        'publications/publication_form.html',
        {
            'form': form,
            'formset': formset,
            'action': action
        }
    )


@login_required
def publication_details(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    return render(request, 'publications/publication_details.html', {'publication': publication})


@login_required
def confirm_publication_details(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            publication = Publication.objects.get(id=request.POST['publication_id'])
        except (KeyError, Publication.DoesNotExist):
            pass
        else:
            Publication.objects.filter(id=publication.id).update(confirmed=True)
            response = json.dumps({"message": "You have successfully confirmed publication details"})
            return HttpResponse(response, content_type='application/json')


@login_required
def manage_author(request, pk=None):
    if pk:
        author = get_object_or_404(Author, pk=pk)
        action = reverse('edit-author', kwargs={'pk': pk})
    else:
        author = Author()
        action = reverse('add-author')
    form = AuthorForm(request.POST or None, instance=author)
    if form.is_valid():
        author = form.save()
        return redirect('detail-author', {'pk': author.pk})
    return render(request, 'publications/author_form.html', {'form': form})


@login_required
def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return render(request, 'publications/author_detail.html', {'author': author})
