# Generated by Django 3.1.2 on 2021-01-14 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vaccine', '0006_auto_20210114_1600'),
    ]

    operations = [
        migrations.RenameField(
            model_name='volunteer',
            old_name='vaccine_group',
            new_name='group',
        ),
    ]