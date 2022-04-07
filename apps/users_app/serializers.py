from rest_framework import  serializers

from apps.users_app.models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

    def update(self,instance, validated_data):
        faviroute_projects = self.validated_data.get('faviroute_projects', None)
        if faviroute_projects:
            if instance.faviroute_projects.filter(id=faviroute_projects[0].id):
                instance.faviroute_projects.remove(faviroute_projects[0].id)
            else:
                instance.faviroute_projects.add(faviroute_projects[0].id)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    class Meta:
        model = User
        fields = ('id','email', 'password', "profile")
        extra_kwargs = {
            "password": {"write_only": True, }
        }
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instancce = self.Meta.model(**validated_data)

        if password is not None:
            instancce.set_password(password)
        instancce.save()
        return instancce

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'is_account_setup')

    def update(self, instance, validated_data):
        # creator = validated_data['creater']
        is_account_setup = validated_data['is_account_setup']
        instance._meta.model(**validated_data)
        instance.save()
        return instance

        # for item in validated_data:
        #     if project._meta.get_field(item):
        #         setattr(instance, item, validated_data[item])
        # Membership.objects.filter(group=instance).delete()

class NestedUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=False)
    name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ["email", "name"]
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['email'] = user.email
        return token

class UserMainSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    class Meta:
        model = User
        fields = ('id','email','name', "profile",'is_admin')
