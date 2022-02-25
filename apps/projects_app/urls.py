from django.urls import path

from apps.projects_app.views import CreatePojectView, UpdateProjectView, GetProjectView, \
    SelectProjectListView, ProjectSearchListView, GetTaskProjects

urlpatterns = [
    path('create-project', CreatePojectView.as_view()),
    path('update-project/<str:pk>', UpdateProjectView.as_view()),
    path('get-project/<str:pk>', GetProjectView.as_view()),
    path('projects/<str:user_id>', SelectProjectListView.as_view()),
    path('get-project/<str:project_id>', GetProjectView.as_view()),
    path('get-search-projects/<str:user_id>/', ProjectSearchListView.as_view()),
    path('get-ticket-projects/<str:ticket_id>', GetTaskProjects.as_view()),

]
