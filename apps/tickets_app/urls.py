from django.urls import path

from apps.tickets_app.views import UpdateTicketView, CreateTicketView, UpdateExtraFieldView, UpdateExtraFieldOptionView

urlpatterns = [
    # path('add-ticket', CreateSectionView.as_view()),
    path('update-ticket/<str:pk>', UpdateTicketView.as_view()),
    path('create-ticket', CreateTicketView.as_view()),
    path('update-extra-field/<str:pk>', UpdateExtraFieldView.as_view()),

    path('update-extra-field-option/<str:pk>', UpdateExtraFieldOptionView.as_view()),


]
