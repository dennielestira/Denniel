# Generated by Django 5.1.1 on 2024-12-19 05:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='hotels/')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('available', models.BooleanField(default=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='rooms/')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='hotel.hotel')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=200)),
                ('customer_email', models.EmailField(max_length=254)),
                ('customer_phone', models.CharField(max_length=15)),
                ('check_in', models.DateField()),
                ('check_out', models.DateField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='hotel.room')),
            ],
        ),
    ]