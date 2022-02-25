from rest_framework import serializers

from apps.projects_app.models import project
from apps.task_section_app.models import Section
from apps.tickets_app.models import Ticket, ExtraField, ExtraFieldOptions
from apps.users_app.models import User
from apps.users_app.serializers import UserSerializer


class ExtraFieldOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraFieldOptions
        fields = ['id', 'title', 'color']

class ExtraFieldSerializer(serializers.ModelSerializer):
    options = ExtraFieldOptionSerializer(required=False, many=True, read_only=False)
    class Meta:
        model = ExtraField
        fields = ['id', 'title', 'value', 'type', 'description','color', 'options','field_option_id']


class TicketSerializer(serializers.ModelSerializer):
    extra_fields = ExtraFieldSerializer(required=False, many=True, read_only=False)
    # projects =ProjectSerializer(required=False, many=True, read_only=True)
    class Meta:
        model = Ticket
        fields = ['id', 'title', 'extra_fields', 'created_by', 'assignee', 'section','project',
                  'description', 'question_or_update', 'is_completed', 'created_at', 'updated_at'
                  ]
        # depth = 1

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        instance.sections.add(validated_data['section'].id)
        instance.projects.add(validated_data['project'].id)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        projects = self.initial_data.get('projects', None)
        sections = self.initial_data.get('sections', None)
        if projects and sections:
            # project_ids = []
            # for project in projects:
                try:
                    # project_ids.append(project)
                    instance.projects.add(projects[0])
                    project_sections = project.objects.filter(id=projects[0]).first().sections.all()
                    if project_sections:
                        project_sections_id = project_sections[0].id
                    else:
                        section = Section.objects.create(title='', project_id=projects[0])
                        project_sections_id = section.id

                    instance.sections.remove(sections[1])
                    instance.sections.add(str(project_sections_id))
                except Exception as e:
                    print('email does not exist')

        elif not projects and sections:
            instance.sections.remove(sections[1])
            instance.sections.add(sections[0])
        instance.save()
        return instance




