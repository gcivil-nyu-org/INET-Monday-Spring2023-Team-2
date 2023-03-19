# Generated by Django 3.2.8 on 2023-03-18 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('opportunityboard', '0003_auto_20230317_2303'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='opportunity',
            options={'verbose_name_plural': 'opportunities'},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'verbose_name_plural': 'subcategories'},
        ),
        migrations.AlterModelOptions(
            name='subsubcategory',
            options={'verbose_name_plural': 'subsubcategories'},
        ),
        migrations.AddField(
            model_name='subsubcategory',
            name='grandparent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='opportunityboard.category'),
        ),
    ]