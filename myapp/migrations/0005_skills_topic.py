# Generated by Django 5.1.1 on 2024-09-11 17:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_course_skills'),
    ]

    operations = [
        migrations.CreateModel(
            name='skills_topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter', models.CharField(max_length=100)),
                ('course_name', models.ForeignKey(db_column='course_name', on_delete=django.db.models.deletion.CASCADE, to='myapp.course')),
                ('course_skills_name', models.ForeignKey(db_column='course_skills_name', on_delete=django.db.models.deletion.CASCADE, to='myapp.course_skills')),
            ],
        ),
    ]