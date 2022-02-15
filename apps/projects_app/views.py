from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.projects_app.models import project
from apps.projects_app.serializers import ProjectSerializer, SelectProjectsSerializer
from apps.task_section_app.serializers import SectionSerializer
from apps.tickets_app.serializers import TicketSerializer
from apps.users_app.models import User


class CreatePojectView(APIView):
    def post(self, request):
        section_data = ''
        task_data = ''
        try:
            section_data = request.data.pop('section_data')
            task_data = request.data.pop('task_data')
        except Exception as e:
            print('project does not created')
        projectSerializer = ProjectSerializer(data=request.data)
        projectSerializer.is_valid(raise_exception=True)
        projectSerializer.save()
        project_id = projectSerializer.data['id']
        if section_data:
            section_data = self.add_porject_id(section_data, project_id)

            section_serializer = SectionSerializer(data=section_data, many=True)
            if section_serializer.is_valid(raise_exception=True):
                 section_serializer.save()

        if task_data:
            task_data = self.add_porject_id(task_data, project_id)
            task_data = self.add_user_id(task_data, request.user.id)

            task_serializer = TicketSerializer(data=task_data, many=True)
            if task_serializer.is_valid(raise_exception=True):
                task_serializer.save()
        user = User.objects.get(id=request.user.id)
        user.is_account_setup = True
        user.save()

        return Response({
            'project': projectSerializer.data
        })


    def add_porject_id(self, data, project_id):
        for item in data:
            item['project'] = project_id
        return  data

    def add_user_id(self, data, user_id):
        for item in data:
            item['created_by'] = user_id
        return data


# class UpdateProjectView(APIView):
#     def put(self, request, id):
#         porject_obj = project.objects.filter(id=id)
#
#         projectSerializer = ProjectSerializer(porject_obj, data=request.data)
#
#         if  projectSerializer.is_valid(raise_exception=True):
#            projectSerializer.save()
#
#
#         return Response({
#             'project': porject_obj
#         })
#
#     def patch(self, request, id):
#         section_data = ''
#         porject_obj = project.objects.filter(id=id).first()
#
#         projectSerializer = ProjectSerializer(porject_obj, data=request.data)
#
#         if projectSerializer.is_valid(raise_exception=True):
#             projectSerializer.save()
#
#         return Response({
#             'project': projectSerializer.data
#         })


class UpdateProjectView(UpdateAPIView):
    queryset = project.objects.all()
    serializer_class = ProjectSerializer

class  SelectProjectListView(ListAPIView):
    # lookup_field = 'creator'
    queryset = project.objects.all()
    # permission_classes = [IsAuthenticated]
    serializer_class = SelectProjectsSerializer
    def get_queryset(self):

        queryset = project.objects.filter(Q(creator=self.kwargs['user_id'])|
                                          Q(members__id=self.kwargs['user_id'])
                                          )
        return set(queryset)


class GetProjectView(RetrieveAPIView):
    queryset = project.objects.all()
    serializer_class = SelectProjectsSerializer

    def get_queryset(self):
        return project.objects.filter(id=self.kwargs['pk'])

