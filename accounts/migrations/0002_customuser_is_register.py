# Generated by Django 3.2.20 on 2023-07-13 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_register',
            field=models.BooleanField(default=False, verbose_name='register'),
        ),
    ]