# Generated by Django 3.2.8 on 2023-04-06 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatroom', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='private',
            field=models.BooleanField(default=False),
        ),
    ]
