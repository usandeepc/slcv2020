from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.views.generic import View
from django.shortcuts import render
from rest_framework.response import Response
import io
from django.http import HttpResponse
from json import *
from vaccine.models import Volunteer
from vaccine.serializers import (RegisterSerializer,
                    LoginSerializer,
                    VoluteerDashboardSerializer,
                    CountSerializer
)
from rest_framework import generics
from rest_framework.filters import SearchFilter


# Create your views here.
class Login(viewsets.ModelViewSet):
    serializer_class = LoginSerializer
    queryset = Volunteer.objects.all()


class Register(viewsets.ModelViewSet):
    serializer_class = RegisterSerializer
    queryset = Volunteer.objects.all()


class VolunteerDashboard(viewsets.ModelViewSet):
    serializer_class = VoluteerDashboardSerializer
    queryset = Volunteer.objects.all()


class Count(viewsets.ModelViewSet):
    serializer_class = CountSerializer
    renderer_classes = [JSONRenderer]
    def get_queryset(self):
        queryset = Volunteer.objects.all()
        qs = queryset.count()
        status = Volunteer.objects.filter(status = 'Positive')
        qs1 = status.count()
        qs2 = qs-qs1
        return queryset
        


class Filter_Data(generics.ListAPIView):
    #queryset = Volunteer.objects.all()
    serializer_class = CountSerializer
    def get_queryset(self):
        
        group = self.request.GET.get('group')
        dose = self.request.GET.get('dose')
        print(group)
        print(type(group))
        qs = Volunteer.objects.all().filter(group=group).filter(dose = dose)
        return qs