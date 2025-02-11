# Generated by Django 5.1.4 on 2025-02-11 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('communityId', models.AutoField(primary_key=True, serialize=False)),
                ('communityTitle', models.CharField(max_length=100)),
                ('communityContent', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateField()),
            ],
        ),
    ]
