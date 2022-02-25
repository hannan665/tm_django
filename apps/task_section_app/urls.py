from django.urls import path

from apps.task_section_app.views import CreateSectionView, UpdateSectionView, GetTaskSections

urlpatterns = [
    path('add-section', CreateSectionView.as_view()),
    path('update-section/<str:pk>', UpdateSectionView.as_view()),
    path('get-ticket-sections/<str:section_tickets>', GetTaskSections.as_view()),

]
