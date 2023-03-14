# Generated by Django 3.2.8 on 2023-03-14 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
        ('jobboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.organization'),
        ),
    ]
