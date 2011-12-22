import simplejson

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, NoReverseMatch
from django.http import (HttpResponse, HttpResponseRedirect,
                         Http404, HttpResponsePermanentRedirect)
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic.list_detail import object_list, object_detail

from core.views import serve_docs
from projects.models import Project
from projects.utils import highest_version


from taggit.models import Tag

def project_index(request, username=None, tag=None):
    """
    The list of projects, which will optionally filter by user or tag,
    in which case a 'person' or 'tag' will be added to the context
    """
    queryset = Project.objects.live()
    if username:
        user = get_object_or_404(User, username=username)
        queryset = queryset.filter(user=user)
    else:
        user = None

    if tag:
        tag = get_object_or_404(Tag, slug=tag)
        queryset = queryset.filter(tags__name__in=[tag.slug])
    else:
        tag = None

    return object_list(
        request,
        queryset=queryset,
        extra_context={'person': user, 'tag': tag},
        page=int(request.GET.get('page', 1)),
        template_object_name='project',
    )

def slug_detail(request, project_slug, filename):
    """
    A detail view for a project with various dataz
    """
    version_slug = 'latest'
    if not filename:
        filename = "index.html"
    split_filename = filename.split('/')
    if len(split_filename) > 1:
        version = split_filename[1]
        proj = get_object_or_404(Project, slug=project_slug)
        valid_version = proj.versions.filter(slug=version).count()
        if valid_version:
            version_slug = version
            filename = '/'.join(split_filename[1:])
    return serve_docs(request=request, project_slug=project_slug, version_slug=version, filename=filename)

def project_detail(request, project_slug):
    """
    A detail view for a project with various dataz
    """
    project = get_object_or_404(Project, slug=project_slug)
    return render_to_response(
        'projects/project_detail.html',
        {
            'project': project,
        },
        context_instance=RequestContext(request),
    )

def legacy_project_detail(request, username, project_slug):
    return HttpResponsePermanentRedirect(reverse(
        project_detail, kwargs = {
            'project_slug': project_slug,
        }
    ))

def tag_index(request):
    """
    List of all tags by most common
    """
    tag_qs = Project.tags.most_common()
    return object_list(
        request,
        queryset=tag_qs,
        page=int(request.GET.get('page', 1)),
        template_object_name='tag',
        template_name='projects/tag_list.html',
    )

def search(request):
    """
    our ghetto site search.  see roadmap.
    """
    if 'q' in request.GET:
        term = request.GET['q']
    else:
        raise Http404
    queryset = Project.objects.live(name__icontains=term)
    if queryset.count() == 1:
        return HttpResponseRedirect(queryset[0].get_absolute_url())

    return object_list(
        request,
        queryset=queryset,
        template_object_name='term',
        extra_context={'term': term},
        template_name='projects/search.html',
    )

def search_autocomplete(request):
    """
    return a json list of project names
    """
    if 'term' in request.GET:
        term = request.GET['term']
    else:
        raise Http404
    queryset = Project.objects.live(name__icontains=term)[:20]

    project_names = queryset.values_list('name', flat=True)
    json_response = simplejson.dumps(list(project_names))

    return HttpResponse(json_response, mimetype='text/javascript')



def subdomain_handler(request, lang_slug=None, version_slug=None, filename=''):
    """
    This provides the fall-back routing for subdomain requests.

    This was made primarily to redirect old subdomain's to their version'd brothers.
    """
    if not filename:
        filename = "index.html"
    project = get_object_or_404(Project, slug=request.slug)
    if version_slug is None:
        #Handle / on subdomain.
        default_version = project.get_default_version()
        url = reverse(serve_docs, kwargs={
            'version_slug': default_version,
            'lang_slug': 'en',
            'filename': filename
        })
        return HttpResponseRedirect(url)
    if version_slug and lang_slug is None:
        #Handle /version/ on subdomain.
        aliases = project.aliases.filter(from_slug=version_slug)
        #Handle Aliases.
        if aliases.count():
            if aliases[0].largest:
                highest_ver = highest_version(project.versions.filter(slug__contains=version_slug, active=True))
                version_slug = highest_ver[0].slug
            else:
                version_slug = aliases[0].to_slug
            url = reverse(serve_docs, kwargs={
                'version_slug': version_slug,
                'lang_slug': 'en',
                'filename': filename
            })
        else:
            try:
                url = reverse(serve_docs, kwargs={
                    'version_slug': version_slug,
                    'lang_slug': 'en',
                    'filename': filename
                })
            except NoReverseMatch:
                raise Http404
        return HttpResponseRedirect(url)
    return serve_docs(request=request,
                      project_slug=project.slug,
                      lang_slug=lang_slug,
                      version_slug=version_slug,
                      filename=filename)
