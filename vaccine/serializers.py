from rest_framework.serializers import ModelSerializer
from vaccine.models import Volunteer


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = Volunteer
        fields = ['email','password','full_name','gender','age','address','health_info',]


class LoginSerializer(ModelSerializer):
    class Meta:
        model = Volunteer
        fields = ['email','password',]


class VoluteerDashboardSerializer(ModelSerializer):
    class Meta:
        model = Volunteer
        fields = '__all__'


class CountSerializer(ModelSerializer):
    class Meta:
        model = Volunteer
        fields = '__all__'


