# Generated by Django 5.0.4 on 2024-05-07 14:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0004_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AccessoryID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accessory', to='WebApp.accessories')),
                ('UserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='WebApp.users')),
            ],
        ),
    ]
