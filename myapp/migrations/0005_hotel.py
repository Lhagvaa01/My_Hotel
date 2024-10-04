# Generated by Django 5.0.4 on 2024-10-03 10:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_hotelowner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('contact', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=255)),
                ('map_url', models.URLField(blank=True, null=True)),
                ('gst_number', models.CharField(blank=True, max_length=100, null=True)),
                ('food_gst_percentage', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('room_gst_percentage', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('joined_date', models.DateTimeField()),
                ('hotel_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.hotelowner')),
            ],
        ),
    ]
