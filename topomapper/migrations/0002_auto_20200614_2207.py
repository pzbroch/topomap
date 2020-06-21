# Generated by Django 2.2.10 on 2020-06-14 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topomapper', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='is_root',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='device',
            name='root_routes',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]