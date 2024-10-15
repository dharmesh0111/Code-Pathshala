# Generated by Django 5.1.1 on 2024-09-11 16:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratings', models.CharField(blank=True, max_length=1, null=True)),
                ('review', models.CharField(blank=True, default='no feedback given', max_length=500, null=True)),
                ('E_learning_id', models.ForeignKey(db_column='E_learning_id', on_delete=django.db.models.deletion.CASCADE, to='myapp.e_learning')),
                ('uid', models.ForeignKey(db_column='uid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
