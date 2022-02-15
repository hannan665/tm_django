
from rest_framework import  serializers

from apps.task_section_app.models import Section
from apps.tickets_app.models import Ticket
from apps.tickets_app.serializers import TicketSerializer


class SectionSerializer(serializers.ModelSerializer):
    ticket_set = TicketSerializer( required=False,many=True ,read_only=False)
    class Meta:
        model = Section
        fields = ('id','title', 'project', 'ticket_set')

    def create(self, validated_data):
        # creator = validated_data['creater']

        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    def validate(self, attrs):
        # genre = attrs.get('genre', [])

        return attrs