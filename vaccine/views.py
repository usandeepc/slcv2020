from rest_framework import viewsets
from django.core import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.views.generic import View
from django.shortcuts import render
from rest_framework.response import Response
import io
import json
from django.http import HttpResponse,JsonResponse
from json import *
from vaccine.models import Volunteer,Maker
from vaccine.serializers import (RegisterSerializer,
                    LoginSerializer,
                    VoluteerDashboardSerializer,
                    CountSerializer,
                    MakerSerializer
)
from rest_framework import generics
from rest_framework.filters import SearchFilter


# Create your views here.
class Register(viewsets.ModelViewSet):
    serializer_class = RegisterSerializer
    queryset = Volunteer.objects.all()
    #def list(self, request, *args, **kwargs):
        #return HttpResponse(json.dumps({'Message':'method not supported'}),content_type = 'application/json')
   # def retrieve(self, request, pk=None):
       # return HttpResponse(json.dumps({'Message':'method not supported'}),content_type = 'application/json')
    def update(self, request, pk=None):
        return HttpResponse(json.dumps({'Message':'method not supported'}),content_type = 'application/json')
    def partial_update(self, request, pk=None):
        return HttpResponse(json.dumps({'Message':'method not supported'}),content_type = 'application/json')
    def destroy(self, request, pk=None):
        return HttpResponse(json.dumps({'Message':'method not supported'}),content_type = 'application/json')


class Login(viewsets.ModelViewSet):
    serializer_class = LoginSerializer
    def list(self, request, *args, **kwargs):
        email = self.request.query_params.get('email')
        password = self.request.query_params.get('password')
        if email is None or password is None:
            return HttpResponse(json.dumps({ "error_message":"No Email and Passord inquery string."}),content_type = 'application/json')
        elif not Volunteer.objects.filter(email = email, password = password).exists():
            return HttpResponse(json.dumps({ "error_message":"No Such user/Password"}),content_type = 'application/json')
        else:
            return HttpResponse(json.dumps({ "error_message":"authsuccesful"}),content_type = 'application/json') 




class VolunteerDashboard(viewsets.ModelViewSet):
    serializer_class = VoluteerDashboardSerializer
    def get_queryset(self):
        email = self.request.query_params.get('email')
        if email is None:
        #    return HttpResponse(json.dumps({'Message':'please provide required details in query string'}),content_type = 'application/json')
            qs = Volunteer.objects.none()
        elif not Volunteer.objects.filter(email = email).exists():
        #    return HttpResponse(json.dumps({'Message':'No user found with given details'}),content_type = 'application/json')
            qs = Volunteer.objects.none()
            
        else:
            qs = Volunteer.objects.all().filter(email = email)
        return qs


class AllResult(viewsets.ModelViewSet):
    serializer_class = CountSerializer
    #renderer_classes = [JSONRenderer]1
    
 
    def list(self, request, *args, **kwargs):
        queryset = Volunteer.objects.all()
        volunteers = queryset.count()
        positive_data = Volunteer.objects.filter(status = 'Positive')
        positives = positive_data.count()
        positive_a = Volunteer.objects.filter(status = 'Positive').filter(group = 'A').count()
        positive_b = Volunteer.objects.filter(status = 'Positive').filter(group = 'B').count()
        threshold = 0
        efficacy_rate =(positive_b-positive_a)/positive_b
        vaccine = 'B'
        if vaccine == 'A':
            s = [
                    {
                        "name" : "slcv2020",
                        "type" : "vaccine",
                        "vaccinegroup" : "A",
                        "efficacy_rate" : {efficacy_rate},
                        "result" : {
                            "volunteer" : {volunteers},
                            "confirm_positive" :{positive_a}
                        }
                    },
                    {
                        "name" : "unknown",
                        "type" : "placebo",
                        "vaccinegroup" : "B",
                        "result" : {
                            "volunteer" : {volunteers},
                            "confirm_positive" :{positive_b}
                        }
                    }
                ]
        elif vaccine == 'B':
            s = [
                    {
                        "name" : "unknown",
                        "type" : "placebo",
                        "vaccinegroup" : "A",
                        "efficacy_rate" : {efficacy_rate},
                        "result" : {
                            "volunteer" : {volunteers},
                            "confirm_positive" :{positive_a}
                        }
                    },
                    {
                        "name" : "SLCV2020",
                        "type" : "vaccine",
                        "vaccinegroup" : "B",
                        "result" : {
                            "volunteer" : {volunteers},
                            "confirm_positive" :{positive_b}
                        }
                    }
                ]

        p = str(s)
        if positives>threshold :
            return HttpResponse(p ,content_type = 'application/json')
        else:
            return HttpResponse(json.dumps({ "error_message":"Phase 3 Trial in progress, please wait."}),content_type = 'application/json')
            


class Result(viewsets.ModelViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = CountSerializer
    def list(self, request, *args, **kwargs):
        group = self.request.GET.get('group')
        dose = self.request.GET.get('dose')
        vaccine='A'
        
        total_groupa_count = Volunteer.objects.all().filter(group='A').filter(dose = dose).filter(status ='Positive').count()
        total_groupb_count = Volunteer.objects.all().filter(group='B').filter(dose = dose).filter(status ='Positive').count()
        positive_count =  Volunteer.objects.all().filter(status ='Positive').count()
        total_count =  Volunteer.objects.all().count()
        total_groupa_count= 2
        total_groupb_count= 8
        efficacy_rate = (total_groupb_count - total_groupa_count)/total_groupb_count
        threshold = 0
        if group == vaccine and positive_count>threshold:
            s =[
                    {
                        "name":"SLCV2020",
                        "type":"vaccine",
                        "vaccineGroup":{group},
                        "dose":{dose},
                        "efficacy_rate":{efficacy_rate},
                        "result":{
                            "volunteer":{total_count},
                            "confirm_positive":{positive_count}
                                }
                    }
                ]
            p = str(s)
            return HttpResponse(json.dumps(p), content_type = 'application/json')
        elif positive_count<threshold :
            return HttpResponse(json.dumps({ "error_message":"Phase 3 Trial in progress, please wait."}),content_type = 'application/json')
        else:
            return HttpResponse(json.dumps({ "error_message":"Group is placebo type,Efficacy cannot be calculated"}),content_type = 'application/json')

class LoginMakerViewset(viewsets.ModelViewSet):
    queryset = Maker.objects.all()
    serializer_class = MakerSerializer
    def list(self, request, *args, **kwargs):
        email = self.request.query_params.get('email')
        password = self.request.query_params.get('password')
        if email is None or password is None:
            return HttpResponse(json.dumps({ "error_message":"No Email and Passord inquery string."}),content_type = 'application/json')
        elif not Maker.objects.filter(email = email, password = password).exists():
            return HttpResponse(json.dumps({ "error_message":"No Such user/Password"}),content_type = 'application/json')
        else:
            return HttpResponse(json.dumps({ "error_message":"authsuccesful"}),content_type = 'application/json')

class RegisterMakerViewset(viewsets.ModelViewSet):
    queryset = Maker.objects.all()
    serializer_class = MakerSerializer
  

class MakerDashboard(viewsets.ModelViewSet):
    def list(self,request, *args, **kwargs):
        total_count = Volunteer.objects.all().count()
        total_positive_count = Volunteer.objects.filter(status ='Positive').count()
        s = {"total_volunteets_count": total_count, "total_positive_volunteets_count": total_positive_count}
        return HttpResponse(json.dumps(str(s)),content_type = 'application/json')


class MakerDashboardFull(viewsets.ModelViewSet):
    def list(self,request, *args, **kwargs):
        total_count = Volunteer.objects.all().count()
        total_positive_count = Volunteer.objects.filter(status ='Positive').count()