# Generated by Django 5.0.6 on 2024-05-23 11:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0006_orders_address_orders_phonenumber'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='accessories',
            name='Followes',
            field=models.ManyToManyField(related_name='accessories', to=settings.AUTH_USER_MODEL),
        ),
    ]
