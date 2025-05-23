# Generated by Django 5.2 on 2025-05-21 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_order_created_at_order_modified_at_part_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='part_images/'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='part',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='part',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
