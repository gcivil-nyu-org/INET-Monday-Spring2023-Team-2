# Generated by Django 4.1.7 on 2023-03-30 07:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("opportunityboard", "0012_merge_20230330_0702"),
    ]

    operations = [
        migrations.AlterField(
            model_name="opportunity",
            name="photo",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
    ]