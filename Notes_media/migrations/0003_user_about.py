# Generated by Django 4.2.1 on 2023-11-22 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notes_media', '0002_alter_user_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='about',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
