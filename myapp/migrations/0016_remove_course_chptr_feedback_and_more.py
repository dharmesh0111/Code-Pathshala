# Generated by Django 5.1.1 on 2024-09-28 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_course_chptr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course_chptr',
            name='feedback',
        ),
        migrations.RemoveField(
            model_name='course_chptr',
            name='rating',
        ),
    ]
