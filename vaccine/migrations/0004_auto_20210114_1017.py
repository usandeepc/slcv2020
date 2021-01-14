# Generated by Django 3.1.2 on 2021-01-14 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaccine', '0003_auto_20210113_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='dose',
            field=models.CharField(choices=[('0.5', 'Half Dose'), ('1', 'Full Dose')], default=None, max_length=4),
        ),
    ]
