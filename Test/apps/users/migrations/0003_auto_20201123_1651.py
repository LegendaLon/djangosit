# Generated by Django 3.1 on 2020-11-23 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20201123_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='rank',
            field=models.CharField(blank=True, default='Новичек', max_length=50, verbose_name='Ранг'),
        ),
        migrations.AddField(
            model_name='profile',
            name='status',
            field=models.CharField(blank=True, max_length=50, verbose_name='Статус'),
        ),
    ]