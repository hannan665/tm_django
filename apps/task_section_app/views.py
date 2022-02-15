from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView, UpdateAPIView

from apps.task_section_app.models import Section
from apps.task_section_app.serializers import SectionSerializer


class CreateSectionView(CreateAPIView):
    serializer_class = SectionSerializer


class UpdateSectionView(UpdateAPIView):
    serializer_class = SectionSerializer
    queryset = Section.objects.all()