# Generated by Django 4.2.3 on 2023-08-19 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='saved_image_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
