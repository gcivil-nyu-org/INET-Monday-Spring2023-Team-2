# Generated by Django 3.2.8 on 2023-04-10 19:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_alter_badge_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='hours_volunteered',
            field=models.DurationField(default=datetime.timedelta(0), null=True),
        ),
    ]