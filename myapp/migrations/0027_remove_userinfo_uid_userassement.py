# Generated by Django 5.1.1 on 2024-10-09 16:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0026_remove_assesment_uid'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='uid',
        ),
        migrations.CreateModel(
            name='USerassement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct_anw', models.IntegerField()),
                ('wrong_anw', models.IntegerField()),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('score', models.FloatField()),
                ('course_name', models.ForeignKey(db_column='course__name', on_delete=django.db.models.deletion.CASCADE, to='myapp.course')),
                ('uid', models.ForeignKey(db_column='uid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
