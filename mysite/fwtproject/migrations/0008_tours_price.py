# Generated by Django 3.0.3 on 2020-04-02 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fwtproject', '0007_bookings'),
    ]

    operations = [
        migrations.AddField(
            model_name='tours',
            name='price',
            field=models.IntegerField(default=0, max_length=7),
            preserve_default=False,
        ),
    ]