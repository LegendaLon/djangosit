# Generated by Django 3.1 on 2020-11-21 12:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('BasePage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания'),
        ),
    ]
