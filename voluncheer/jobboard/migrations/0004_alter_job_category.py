# Generated by Django 4.1.7 on 2023-03-09 05:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("jobboard", "0003_alter_job_category_alter_job_pubdate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="category",
            field=models.CharField(
                choices=[
                    ("sports", "Sports"),
                    ("environment", "Environment"),
                    ("healthcare", "Healthcare"),
                    ("community", "Community"),
                    ("animals", "Animal"),
                ],
                max_length=20,
            ),
        ),
    ]
