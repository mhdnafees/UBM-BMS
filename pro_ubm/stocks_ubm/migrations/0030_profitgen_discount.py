# Generated by Django 3.0.3 on 2020-07-25 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks_ubm', '0029_auto_20200725_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='profitgen',
            name='discount',
            field=models.IntegerField(default=0),
        ),
    ]
