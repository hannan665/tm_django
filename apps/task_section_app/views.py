from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView

from apps.task_section_app.models import Section
from apps.task_section_app.serializers import SectionSerializer


class CreateSectionView(CreateAPIView):
    serializer_class = SectionSerializer


class UpdateSectionView(UpdateAPIView):
    serializer_class = SectionSerializer
    queryset = Section.objects.all()


class GetTaskSections(ListAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    lookup_field = 'section_tickets'

    def get_queryset(self):
        return Section.objects.filter(section_tickets=self.kwargs['section_tickets'])
