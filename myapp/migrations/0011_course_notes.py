# Generated by Django 5.1.1 on 2024-09-14 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_course_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='notes',
            field=models.FileField(default=None, max_length=250, null=True, upload_to='media'),
        ),
    ]