# Generated by Django 3.1 on 2020-12-16 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0002_auto_20201216_1909'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
    ]