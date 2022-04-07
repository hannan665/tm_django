
from rest_framework import  serializers

from apps.projects_app.models import project
from apps.task_section_app.models import Section
from apps.task_section_app.serializers import SectionSerializer
from apps.tickets_app.serializers import TicketSerializer
from apps.users_app.models import User
from apps.users_app.serializers import UserSerializer, NestedUserSerializer, UserMainSerializer, UserProfileSerializer


class ProjectSerializer(serializers.ModelSerializer):
    # members = serializers.ListField(write_only=True, required=False)
    members = UserMainSerializer(many=True, required=False)
    # members = UserSerializer(required=False,many=True)
    # section = SectionSerializer(many=True, required=False, source="title")
    sections = SectionSerializer(many=True, required=False,read_only=False)


    class Meta:
        model = project
        # fields = ["members"]
        fields = ["id","title","creator","members","description","type","sections","color"]
        extra_kwargs = {'members': {'required': False}}

    def create(self, validated_data):
        # creator = validated_data['creater']

        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance


    def update(self, instance, validated_data):
        # creator = validated_data['creater']
        members_email = validated_data['members']
        member_ids = []
        for email in members_email:

            email = email['email']
            try:
                user = User.objects.get(email=email)
                member_ids.append(user.id)
                instance.members.add(user.id)

            except Exception as e:
               print('email does not exist')
        # instance.members.set(member_ids)
        instance.save()
        return instance



class SelectProjectsSerializer(serializers.ModelSerializer):
    # members = NestedUserSerializer(many=True, required=False)
    members = UserSerializer( required=False, many=True)
    sections = SectionSerializer(many=True, required=False,read_only=False)
    project_tickets = TicketSerializer(required=False, many=True, read_only=False)
    # faviroute_projects = UserProfileSerializer(required=False, read_only=False, many=True)


    class Meta:
        model = project
        # fields = ["members"]
        fields = ["id","title","creator","members","description", "type", 'color',"sections", 'project_tickets','faviroute_projects']
        extra_kwargs = {'members': {'required': False}}
