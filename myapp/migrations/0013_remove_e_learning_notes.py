# Generated by Django 5.1.1 on 2024-09-14 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_coursefeedback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='e_learning',
            name='notes',
        ),
    ]