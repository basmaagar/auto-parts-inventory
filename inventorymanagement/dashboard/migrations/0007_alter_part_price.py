# Generated by Django 5.2 on 2025-05-14 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_remove_part_type_part_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='price',
            field=models.IntegerField(default=100, verbose_name='Price'),
        ),
    ]
