from django.contrib import admin
from vaccine.models import Volunteer

# Register your models here.
class VolunteerAdmin(admin.ModelAdmin):
    list_display =['email','password','full_name','gender','address','health_info','group','dose','status',]


admin.site.register(Volunteer,VolunteerAdmin);
