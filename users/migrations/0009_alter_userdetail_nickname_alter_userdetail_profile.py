# Generated by Django 5.1.6 on 2025-03-05 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_userdetail_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='nickname',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='profile',
            field=models.ImageField(blank=True, default='profile/default.jpg', null=True, upload_to='profile/'),
        ),
    ]
