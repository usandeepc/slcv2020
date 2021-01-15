from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.views.generic import View
from django.shortcuts import render
from rest_framework.response import Response
import io
import json
from django.http import HttpResponse,JsonResponse
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
    #renderer_classes = [JSONRenderer]
    
 
    def list(self, request, *args, **kwargs):
        queryset = Volunteer.objects.all()
        volunteers = queryset.count()
        positive_data = Volunteer.objects.filter(status = 'Positive')
        positives = positive_data.count()
        positive_a = Volunteer.objects.filter(status = 'Positive').filter(group = 'A').count()
        positive_b = Volunteer.objects.filter(status = 'Positive').filter(group = 'B').count()
        threshold = 0
        efficacy_rate =(positive_b-positive_a)/positive_b
        
        if positives>threshold :
            return HttpResponse(json.dumps({'Message':'Vaccination in progress'}),content_type = 'application/json')
        else:
            return HttpResponse(json.dumps({'Message':'Vaccination in progress'}),content_type = 'application/json')
            


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

