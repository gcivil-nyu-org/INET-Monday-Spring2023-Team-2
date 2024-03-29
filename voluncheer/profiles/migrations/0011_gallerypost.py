# Generated by Django 3.2.8 on 2023-04-15 17:59

from django.db import migrations, models
import django.db.models.deletion
import profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_alter_volunteer_hours_volunteered'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=profiles.models._post_photo_path)),
                ('content', models.TextField(default='', help_text='Caption your photo')),
                ('author', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='author', to='profiles.volunteer')),
                ('volunteer', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.volunteer')),
            ],
        ),
    ]
