from django.urls import path

from apps.projects_app.views import UpdateProjectView
from apps.users_app.serializers import UserProfileSerializer
from apps.users_app.views import Register, LoginViewCookie, UserGetCookie, LogoutViewCookie, UserUpdate, GetUserView, \
    UserListView, UpdateUserProfile

urlpatterns = [
    path('register', Register.as_view()),
    path('login', LoginViewCookie.as_view(), name="login"),
    path('users', UserGetCookie.as_view()),
    path('logout', LogoutViewCookie.as_view()),
    path('update-user/<str:pk>', UserUpdate.as_view()),
    path('get-user/<str:pk>', GetUserView.as_view()),
    # path('get-user/<str:pk>', GetUserView.as_view()),
    path('get-members/<str:project_id>/', UserListView.as_view()),
    path('update-profile/<str:id>', UpdateUserProfile.as_view()),
]
