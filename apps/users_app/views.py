import datetime

import jwt
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework import filters
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import UpdateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse, reverse_lazy
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users_app.models import User, UserProfile
from apps.users_app.serializers import UserSerializer, UserUpdateSerializer, MyTokenObtainPairSerializer, \
    UserProfileSerializer, UserMainSerializer
from tm_django.filters_override import FilterMemberOfProject


class MyObtainTokenPairView(TokenObtainPairView):
    # permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

# @method_decorator(csrf_exempt, name='dispatch')
class Register(APIView):
    def post(self, request):

       email = request.data.get("email", None)
       user = User.objects.filter(email=email).first()
       if not user:
           serializer = UserSerializer(data=request.data)
           serializer.is_valid(raise_exception=True)
           serializer.save()
           payload = {
               "id": serializer.data.get('id'),
               "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
               "iat": datetime.datetime.utcnow()
           }
           # creating token

           token = jwt.encode(payload, 'secret', algorithm='HS256')
           user = User.objects.filter(email=email).first()
           refresh = RefreshToken.for_user(user)
           res = {
               'refresh': str(refresh),
               'access': str(refresh.access_token),
           }

           return Response({
               'token': str(refresh.access_token),
               'refresh': str(refresh),
               "singup_success": True,
               "user": serializer.data

           })

       else:
          raise AuthenticationFailed("Email address already exist.")


class LoginViewCookie(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = User.objects.filter(email=email).first()
        if not user:
            raise AuthenticationFailed("user not found")
        if not user.check_password(password):
            raise AuthenticationFailed("incorrect password")
        is_account_active = user.is_account_setup
        payload = {
            "id": user.uuid,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()
        }
        # creating token
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        responce = Response()
        # save token in cookies
        responce.set_cookie(key='jwt', value=token, httponly=True)
        refresh = RefreshToken.for_user(user)
        # res = {
        #     'refresh': str(refresh),
        #     'access': str(refresh.access_token),
        # }
        responce.data = {
            "jwt": str(refresh.access_token),
            "login_succes": True,
            "isAccountActive": is_account_active,
            "user_id": user.id
        }
        return responce


class UserGetCookie(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")
        if not token:
            raise AuthenticationFailed("unauthenticated user")

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({
            "users": serializer.data
        })


class LogoutViewCookie(APIView):
    def post(self, request):
        token = request.COOKIES.get("jwt")
        if not token:
            raise AuthenticationFailed("login please")
        response = Response()
        response.delete_cookie("jwt")
        response.data = {
            "message": "logout successfully"
        }
        return response


class UserUpdate(APIView):
    # queryset = User.objects.all()
    # serializer_class = UserUpdateSerializer
    def patch(self,request, pk):
        user_ins = User.objects.get(id=pk)
        userser = UserUpdateSerializer(user_ins,data=request.data)
        userser.is_valid(raise_exception=True)
        userser.save()
        return Response({
           'user_updated':True
        })

class GetUserView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserMainSerializer


    def get_queryset(self):
        return User.objects.filter(id=self.kwargs['pk'])


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserMainSerializer
    filter_backends = [FilterMemberOfProject]
    search_fields = ['name', 'email', 'profile__name']
    lookup_field = ['project_id']

    # def filter_queryset(self, queryset):
    #     """
    #     Given a queryset, filter it with whichever filter backend is in use.
    #     You are unlikely to want to override this method, although you may need
    #     to call it either from a list view, or from a custom `get_object`
    #     method if you want to apply the configured filtering backend to the
    #     default queryset.
    #     """
    #     for backend in list(self.filter_backends):
    #         queryset = backend().filter_queryset(self.request, queryset, self)
    #     return queryset

    # def get_queryset(self):
    #     return User.objects.filter(id=self.kwargs['pk'])
