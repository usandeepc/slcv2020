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
                    MakerSerializer,
                    MakerDashboardSerializer
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
    #def update(self, request, pk=None):
    #    return HttpResponse(json.dumps({'Message':'method not supported'}),content_type = 'application/json')
    #def partial_update(self, request, pk=None):
    #    return HttpResponse(json.dumps({'Message':'method not supported'}),content_type = 'application/json')
    #def destroy(self, request, pk=None):
    #    return HttpResponse(json.dumps({'Message':'method not supported'}),content_type = 'application/json')


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
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
    
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
#        positive_a = Volunteer.objects.filter(status = 'Positive').filter(group = 'A').count()
#        positive_b = Volunteer.objects.filter(status = 'Positive').filter(group = 'B').count()
        threshold = 0
#        efficacy_rate =(positive_b-positive_a)/positive_b
        vaccine = 'A'
        if vaccine == 'A':
            positive_a = Volunteer.objects.filter(status = 'Positive').filter(group = 'A').count()
            positive_b = Volunteer.objects.filter(status = 'Positive').filter(group = 'B').count()
            efficacy_rate =(positive_b-positive_a)/positive_b
            s = [
                    {
                        "name" : "slcv2020",
                        "type" : "vaccine",
                        "vaccinegroup" : "A",
                        "efficacy_rate" : {efficacy_rate},
                        "result" : {
                            "volunteer" : volunteers,
                            "confirm_positive" :positive_a
                        }
                    },
                    {
                        "name" : "unknown",
                        "type" : "placebo",
                        "vaccinegroup" : "B",
                        "result" : {
                            "volunteer" : volunteers,
                            "confirm_positive" :positive_b
                        }
                    }
                ]
        elif vaccine == 'B':
            positive_a = Volunteer.objects.filter(status = 'Positive').filter(group = 'B').count()
            positive_b = Volunteer.objects.filter(status = 'Positive').filter(group = 'A').count()
            efficacy_rate =(positive_b-positive_a)/positive_b
            s = [
                    {
                        "name" : "unknown",
                        "type" : "placebo",
                        "vaccinegroup" : "A",
                        "efficacy_rate" : efficacy_rate,
                        "result" : {
                            "volunteer" : volunteers,
                            "confirm_positive" :positive_a
                        }
                    },
                    {
                        "name" : "SLCV2020",
                        "type" : "vaccine",
                        "vaccinegroup" : "B",
                        "result" : {
                            "volunteer" : volunteers,
                            "confirm_positive" :positive_b
                        }
                    }
                ]

        p = str(s)
        if positives>threshold :
            return HttpResponse(json.dumps(p) ,content_type = 'application/json')
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
  

class MakerDashboardFull(viewsets.ModelViewSet):
    def list(self,request, *args, **kwargs):
        vaccine = 'B'
        threshold = 1
        total_count = Volunteer.objects.all().count()
        total_positive_count = Volunteer.objects.filter(status ='Positive').count()

        if vaccine == 'A':
            total_positivea_count = Volunteer.objects.filter(status ='Positive').filter(group='A').count()
            total_positiveb_count = Volunteer.objects.filter(status ='Positive').filter(group='B').count()
        elif vaccine == 'B':
            total_positivea_count = Volunteer.objects.filter(status ='Positive').filter(group='B').count()
            total_positiveb_count = Volunteer.objects.filter(status ='Positive').filter(group='A').count()

        
        efficacy_rate_overall = (total_positiveb_count - total_positivea_count)/total_positiveb_count

        total_positivehalfa_count = Volunteer.objects.filter(status ='Positive').filter(group='A').filter(dose='0.5').count()
        total_positivehalfb_count = Volunteer.objects.filter(status ='Positive').filter(group='B').filter(dose='0.5').count()

        total_positivefulla_count = Volunteer.objects.filter(status ='Positive').filter(group='A').filter(dose='1').count()
        total_positivefullb_count = Volunteer.objects.filter(status ='Positive').filter(group='A').filter(dose='1').count()

        total_positivea_count = Volunteer.objects.filter(status ='Positive').filter(group='A').count()
        total_positiveb_count = Volunteer.objects.filter(status ='Positive').filter(group='B').count()

        efficacy_rate_halfdose = (total_positivehalfb_count-total_positivehalfa_count)/total_positivehalfb_count
        efficacy_rate_fulldose = (total_positivefullb_count-total_positivefulla_count)/total_positivefullb_count

        if total_positive_count < threshold:
            s = {"total_volunteets_count": total_count, "total_positive_volunteets_count": total_positive_count}
        elif total_positive_count >= threshold:
            s = {"total_volunteets_count": total_count,
             "total_positive_volunteers_count": total_positive_count,
             "total_positive_vaccine_group": total_positivea_count,
             "total_positive_placebo_group": total_positiveb_count,
             "efficacy_rate_halfdose" : efficacy_rate_halfdose,
             "efficacy_rate_fulldose" : efficacy_rate_fulldose,
             "efficacyrate_overall" : efficacy_rate_overall,}

        
        return HttpResponse(json.dumps(str(s)),content_type = 'application/json')


class MakerDashboard(viewsets.ModelViewSet):
    serializer_class = MakerDashboardSerializer
    def get_queryset(self):
        email = self.request.query_params.get('email')
        if email is None:
        #    return HttpResponse(json.dumps({'Message':'please provide required details in query string'}),content_type = 'application/json')
            qs = Maker.objects.none()
        elif not Maker.objects.filter(email = email).exists():
        #    return HttpResponse(json.dumps({'Message':'No user found with given details'}),content_type = 'application/json')
            qs = Maker.objects.none()
            
        else:
            qs = Maker.objects.all().filter(email = email)
        return qs

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)