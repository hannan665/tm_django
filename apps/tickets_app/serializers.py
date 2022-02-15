from rest_framework import serializers

from apps.tickets_app.models import Ticket, ExtraField, ExtraFieldOptions

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

    class Meta:
        model = Ticket
        fields = ['id', 'title', 'extra_fields', 'created_by', 'assignee', 'section',
                  'description', 'question_or_update', 'is_completed', 'created_at', 'updated_at'
                  ]

    def create(self, validated_data):
        # creator = validated_data['creater']

        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    # def update(self, instance, validated_data):
    #     # creator = validated_data['creater']
    #
    #     instance = self.Meta.model(**validated_data)
    #     instance.save()
    #     return instance
