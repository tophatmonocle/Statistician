from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from stats.models import Project, Metric


@login_required()
def index(request, project_slug=None):
    if not request.user.email.endswith('@tophatmonocle.com'):
        return redirect('stats.views.unauthorized')

    return render_to_response('index.html', {
        "projects": Project.objects.all()
    });


@login_required()
def project(request, project_slug=None):
    if not request.user.email.endswith('@tophatmonocle.com'):
        return redirect('stats.views.unauthorized')

    return render_to_response('project.html', {
        "username": request.user.username,
        "project": project_slug,
        "projects": Project.objects.all(),
        "metrics": Metric.objects.filter(project__slug=project_slug)
    })


def unauthorized(request):
    return render_to_response('unauthorized.html', {
        "username": request.user.username
    })


@login_required()
def projects(request, project_slug=None):
    if not request.user.email.endswith('@tophatmonocle.com'):
        return redirect('stats.views.unauthorized')
    return render_to_response('projects.html', {
        "username": request.user.username,
        "projects": Project.objects.all()
    })


@login_required()
def graphs(request, project_slug, graph_slug=None):
    return render_to_response('graphs.html', {
        "username": request.user.username,
        "projects": Project.objects.all(),
        "graph": graph_slug,
        "project": project_slug
    })
