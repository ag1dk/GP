# Generated by Django 4.2 on 2024-04-30 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse_platform', '0007_alter_item_latitude_alter_item_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=30, max_digits=40, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=30, max_digits=40, null=True),
        ),
    ]
