# Generated by Django 5.0.4 on 2024-10-04 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_hotel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hotelowner',
            old_name='email_address',
            new_name='email',
        ),
        migrations.AddField(
            model_name='hotelowner',
            name='password',
            field=models.CharField(default=123, max_length=255),
            preserve_default=False,
        ),
    ]
