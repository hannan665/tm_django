from django.db.models import Q
from rest_framework import filters
from apps.projects_app.models import project

class FilterMemberOfProject(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        members = project.objects.filter(id=view.kwargs['project_id']).first().members.all()
        params = request.GET['search']
        qs = members.filter(
            Q(name__icontains=params) |
            Q(email__icontains=params) |
            Q(profile__name__icontains=params)
        )
        return qs

class FilterProject(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        params = request.GET['search']
        if not params:
            members = project.objects.filter(
                Q(creator=view.kwargs['user_id']) |
                Q(members__id=view.kwargs['user_id'])
            )
        else:
            members = project.objects.filter(
                Q(creator=view.kwargs['user_id']) |
                Q(members__id=view.kwargs['user_id'])
            ).filter(
                title__icontains=params
            )

        return members.distinct()

