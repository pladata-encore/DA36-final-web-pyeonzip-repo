# Generated by Django 5.1.6 on 2025-02-13 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_userdetail_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetail',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254),
        ),
    ]
