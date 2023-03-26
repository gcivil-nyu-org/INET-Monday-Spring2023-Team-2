# Generated by Django 3.2.8 on 2023-03-26 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
        ('opportunityboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='opportunity',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.organization'),
        ),
        migrations.AddField(
            model_name='opportunity',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='opportunityboard.subcategory'),
        ),
        migrations.AddField(
            model_name='opportunity',
            name='subsubcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='opportunityboard.subsubcategory'),
        ),
    ]
