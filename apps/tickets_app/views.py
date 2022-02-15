from django.shortcuts import render

# Create your views here.
from rest_framework.generics import UpdateAPIView, CreateAPIView

from apps.tickets_app.models import Ticket, ExtraField
from apps.tickets_app.serializers import TicketSerializer, ExtraFieldSerializer


class UpdateTicketView(UpdateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_queryset(self):

        id = self.kwargs['pk']
        Ticket.objects.filter(id=id).update(**self.request.data)
        t=  Ticket.objects.filter(id=id)
        return t

class UpdateExtraFieldView(UpdateAPIView):
    queryset = ExtraField.objects.all()
    serializer_class = ExtraFieldSerializer

    def get_queryset(self):

        id = self.kwargs['pk']
        ExtraField.objects.filter(id=id).update(**self.request.data)
        t=  ExtraField.objects.filter(id=id)
        return t



class CreateTicketView(CreateAPIView):
    serializer_class = TicketSerializer
