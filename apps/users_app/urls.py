from django.urls import path

from apps.projects_app.views import UpdateProjectView
from apps.users_app.views import Register, LoginViewCookie, UserGetCookie, LogoutViewCookie, UserUpdate

urlpatterns = [
    path('register', Register.as_view()),
    path('login', LoginViewCookie.as_view(), name="login"),
    path('users', UserGetCookie.as_view()),
    path('logout', LogoutViewCookie.as_view()),
    path('update-user/<str:pk>', UserUpdate.as_view()),
]
