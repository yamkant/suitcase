# Generated by Django 3.2.7 on 2023-10-01 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_remove_productfavorite_user_id'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='productprofile',
            table='product_profiles',
        ),
    ]
