# Generated by Django 5.0.4 on 2024-05-22 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("WebApp", "0004_alter_accessories_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accessories",
            name="Image",
            field=models.ImageField(upload_to="static/images/product/"),
        ),
    ]
