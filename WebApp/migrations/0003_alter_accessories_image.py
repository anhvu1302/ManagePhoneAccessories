# Generated by Django 5.0.4 on 2024-05-21 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("WebApp", "0002_remove_orders_address_remove_orders_phonenumber_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accessories",
            name="Image",
            field=models.ImageField(upload_to="static/images/product/"),
        ),
    ]
