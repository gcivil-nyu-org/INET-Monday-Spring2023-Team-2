# Generated by Django 4.1.7 on 2023-03-30 01:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0001_initial"),
        ("opportunityboard", "0008_opportunity_volunteer"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="opportunity",
            name="volunteer",
        ),
        migrations.AddField(
            model_name="opportunity",
            name="volunteer",
            field=models.ManyToManyField(blank=True, null=True, to="profiles.volunteer"),
        ),
    ]