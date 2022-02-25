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
        t=  ExtraField.objects.filter(id=id)
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



