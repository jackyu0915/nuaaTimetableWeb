# Generated by Django 2.2.11 on 2020-03-28 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0004_lesson_info_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson_info',
            name='times',
            field=models.CharField(default='', max_length=32),
        ),
        migrations.AddField(
            model_name='user_info',
            name='times',
            field=models.CharField(default='1', max_length=3),
        ),
    ]