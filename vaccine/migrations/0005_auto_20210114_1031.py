# Generated by Django 3.1.2 on 2021-01-14 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaccine', '0004_auto_20210114_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='dose',
            field=models.CharField(choices=[('0.5', 'Half Dose'), ('1', 'Full Dose')], default='0.5', max_length=4),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='vaccine_group',
            field=models.CharField(choices=[('Group A', 'A'), ('Group B', 'B')], default='Group A', max_length=8),
        ),
    ]
