# Generated by Django 3.2.8 on 2023-03-26 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opportunityboard', '0004_alter_opportunity_pubdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='opportunity',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='opportunity',
            name='frequency',
            field=models.CharField(blank=True, choices=[('weekly', 'Weekly')], max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='opportunity',
            name='is_recurring',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='opportunity',
            name='occurences',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
