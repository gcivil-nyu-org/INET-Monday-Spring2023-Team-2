# Generated by Django 3.2.8 on 2023-03-19 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opportunityboard', '0005_remove_subsubcategory_grandparent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opportunity',
            name='duration',
        ),
        migrations.AddField(
            model_name='opportunity',
            name='end',
            field=models.TimeField(default='12:00:00'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='opportunity',
            name='staffing',
            field=models.PositiveIntegerField(),
        ),
    ]