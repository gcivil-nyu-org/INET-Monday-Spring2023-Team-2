# Generated by Django 3.2.8 on 2023-03-26 04:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opportunityboard', '0005_auto_20230326_0057'),
    ]

    operations = [
        migrations.RenameField(
            model_name='opportunity',
            old_name='frequency',
            new_name='recurrence',
        ),
    ]