# Generated by Django 5.1.6 on 2025-02-13 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_product_convenient_store_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='convenient_store_name',
            field=models.CharField(default='ALL', max_length=10),
        ),
    ]
