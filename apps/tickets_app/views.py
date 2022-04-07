from django.shortcuts import render

# Create your views here.
from rest_framework.generics import UpdateAPIView, CreateAPIView, RetrieveAPIView

from apps.tickets_app.models import Ticket, ExtraField, ExtraFieldOptions
from apps.tickets_app.serializers import TicketSerializer, ExtraFieldSerializer, ExtraFieldOptionSerializer


class UpdateTicketView(UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_queryset(self):
        id = self.kwargs['pk']
        projects = self.request.data.get('projects',None)
        sections = self.request.data.get('sections', None)

        if not projects and not sections:
            Ticket.objects.filter(id=id).update(**self.request.data)
        t = Ticket.objects.filter(id=id)
        return t


class UpdateExtraFieldView(UpdateAPIView):
    queryset = ExtraField.objects.all()
    serializer_class = ExtraFieldSerializer

    def get_queryset(self):
        id = self.kwargs['pk']
        ExtraField.objects.filter(id=id).update(**self.request.data)
        t = ExtraField.objects.filter(id=id)
        return t


class UpdateExtraFieldOptionView(UpdateAPIView):
    queryset = ExtraFieldOptions.objects.all()
    serializer_class = ExtraFieldOptionSerializer

    def get_queryset(self):
        id = self.kwargs['pk']
        ExtraFieldOptions.objects.filter(id=id).update(**self.request.data)
        extra_field_option = ExtraFieldOptions.objects.filter(id=id)
        extra_field = ExtraField.objects.filter(id=extra_field_option[0].extra_field_id).first()
        extra_field.color = self.request.data["color"]
        extra_field.save()
        return extra_field_option


class CreateTicketView(CreateAPIView):
    serializer_class = TicketSerializer

    def perform_create(self, serializer):
        ticket = serializer.save()
        _create_default_extraFields_and_options(ticket)


def _create_default_extraFields_and_options(ticket):
    default_option_data_1 = {
        'title': 'to do',
        'color': '#f06a6a'
    }
    default_option_data_2 = {
        'title': 'in progress',
        'color': '#aecf55'
    }
    extra_field_options = ExtraFieldOptionSerializer(data=[default_option_data_1, default_option_data_2], many=True)
    if extra_field_options.is_valid():
        extra_field_options.save()
        default_field_data_1 = {
            'title': 'To do',
            'color': extra_field_options.data[0]['color'],
            'value': extra_field_options.data[0]['title'],
            'field_option_id': extra_field_options.data[0]['id'],
            'ticket': ticket.id
        }
        default_field_data_2 = {
            'title': 'in progress',
            'color': extra_field_options.data[1]['color'],
            'value': extra_field_options.data[1]['title'],
            'field_option_id': extra_field_options.data[1]['id'],
            'ticket': ticket.id

        }
        extra_fields = ExtraFieldSerializer(data=[default_field_data_1, default_field_data_2], many=True)
        if extra_fields.is_valid():
            extra_fields.save()
            extra_field_option_1 = ExtraFieldOptions.objects.get(id=extra_field_options.data[0]['id'])
            extra_field_option_1.extra_field_id = extra_fields.data[0]['id']
            extra_field_option_2 = ExtraFieldOptions.objects.get(id=extra_field_options.data[1]['id'])
            extra_field_option_2.extra_field_id = extra_fields.data[1]['id']
            extra_field_option_1.save()
            extra_field_option_2.save()


