# Generated by Django 3.2.8 on 2023-04-02 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20230325_2115'),
        ('opportunityboard', '0014_alter_opportunity_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opportunity',
            name='volunteer',
            field=models.ManyToManyField(blank=True, to='profiles.Volunteer'),
        ),
    ]
