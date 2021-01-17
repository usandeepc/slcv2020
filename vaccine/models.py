from django.db import models

# Create your models here.
class Volunteer(models.Model):
    email = models.EmailField(max_length = 64, default = None, unique = True);
    password = models.CharField(max_length = 64, default = None);
    full_name = models.CharField(max_length = 64, default = None);
    age = models.IntegerField(default = None);
    class Gender(models.TextChoices):
        M = 'male'
        F = 'female'
        o = 'others'
    gender = models.CharField(max_length = 8, choices = Gender.choices, default = Gender.M);
    address = models.CharField(max_length = 256, default = None);
    health_info = models.TextField(max_length = 256, default = None);
    class Group(models.TextChoices):
        A = 'A'
        B = 'B'
        C = 'X'
    group = models.CharField(max_length = 8, choices = Group.choices, default = Group.C);
    class Dose(models.TextChoices):
        half_dose = '0.5'
        full_dose = '1'
        none = '0'
    dose = models.CharField(max_length = 4, choices = Dose.choices, default = Dose.none);
    class Status(models.TextChoices):
        P = 'Positive'
        N = 'Negative'
    status = models.CharField(max_length = 10, choices = Status.choices,default = Status.N)


class Maker(models.Model):
    email = models.EmailField(max_length = 64, default = None, unique = True);
    password = models.CharField(max_length = 64, default = None);
    name = models.CharField(max_length = 64, default = None);
    age = models.IntegerField(default = None);
    address = models.CharField(max_length = 256, default = None);