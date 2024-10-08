# Generated by Django 5.0.4 on 2024-10-03 09:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParentMenus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_id', models.IntegerField()),
                ('menu_name', models.CharField(max_length=255)),
                ('menu_url', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='SystemInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system_id', models.CharField(max_length=255)),
                ('system_name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UserInfoUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=255)),
                ('user_pass', models.CharField(max_length=255)),
                ('user_mail', models.EmailField(max_length=254)),
                ('user_phone', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='SuperAdmin1', max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Menus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_id', models.IntegerField()),
                ('menu_name', models.CharField(max_length=255)),
                ('menu_url', models.CharField(max_length=255)),
                ('parent_menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.parentmenus')),
                ('system_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.systeminfo')),
            ],
        ),
        migrations.AddField(
            model_name='parentmenus',
            name='system_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.systeminfo'),
        ),
        migrations.CreateModel(
            name='PermissionsUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_access', models.BooleanField(default=False)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.menus')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.userinfouser')),
            ],
        ),
        migrations.AddField(
            model_name='userinfouser',
            name='user_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.usertype'),
        ),
    ]
