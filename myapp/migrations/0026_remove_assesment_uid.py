# Generated by Django 5.1.1 on 2024-10-09 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0025_alter_assesment_uid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assesment',
            name='uid',
        ),
    ]
