# Generated by Django 2.2.10 on 2020-06-20 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topomapper', '0012_auto_20200620_1740'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='uplinks',
        ),
        migrations.DeleteModel(
            name='Link',
        ),
    ]
