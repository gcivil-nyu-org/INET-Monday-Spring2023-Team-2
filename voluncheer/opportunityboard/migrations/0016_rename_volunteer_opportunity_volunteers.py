# Generated by Django 3.2.8 on 2023-04-02 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opportunityboard', '0015_alter_opportunity_volunteer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='opportunity',
            old_name='volunteer',
            new_name='volunteers',
        ),
    ]
