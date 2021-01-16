# Generated by Django 3.1.2 on 2021-01-16 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaccine', '0008_maker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='dose',
            field=models.CharField(choices=[('0.5', 'Half Dose'), ('1', 'Full Dose'), ('0', 'None')], default='0', max_length=4),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='group',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('X', 'C')], default='X', max_length=8),
        ),
    ]