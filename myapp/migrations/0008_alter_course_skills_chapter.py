# Generated by Django 5.1.1 on 2024-09-12 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_course_skills_chapter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course_skills',
            name='chapter',
            field=models.CharField(default=None, max_length=500),
        ),
    ]
