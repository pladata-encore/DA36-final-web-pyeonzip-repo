# Generated by Django 5.1.6 on 2025-02-13 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_userdetail_age_range'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetail',
            name='profile',
            field=models.ImageField(blank=True, null=True, upload_to='profile/'),
        ),
    ]
