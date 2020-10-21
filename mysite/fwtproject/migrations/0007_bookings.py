# Generated by Django 3.0.3 on 2020-04-02 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fwtproject', '0006_auto_20200401_2009'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=30)),
                ('destination', models.CharField(max_length=50)),
                ('bookingdate', models.CharField(max_length=10)),
                ('dob', models.DateTimeField()),
            ],
        ),
    ]
