# Generated by Django 5.0 on 2024-04-04 14:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_successful',
            name='date_added',
        ),
        migrations.AddField(
            model_name='order_successful',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
