# Generated by Django 4.2.1 on 2023-11-25 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notes_media', '0005_remove_user_category_alter_post_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='full_name',
            field=models.CharField(default='None', max_length=30),
        ),
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.CharField(default='None', max_length=20),
        ),
    ]