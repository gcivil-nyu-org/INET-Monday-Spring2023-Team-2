# Generated by Django 3.2.8 on 2023-04-06 00:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20230405_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='hours_volunteered',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]
