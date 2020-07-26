# Generated by Django 3.0.3 on 2020-07-17 21:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('stocks_ubm', '0016_remove_salesregistry_landing_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesregistry',
            name='sold_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
