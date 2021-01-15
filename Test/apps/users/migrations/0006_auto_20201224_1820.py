# Generated by Django 3.1 on 2020-12-24 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20201223_2035'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='money',
            field=models.IntegerField(default=0, verbose_name='Деньги'),
        ),
        migrations.AddField(
            model_name='profile',
            name='reputation',
            field=models.IntegerField(default=0, verbose_name='Репутация'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='rank',
            field=models.CharField(default='Пользователь', max_length=50, verbose_name='Ранг'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='slug',
            field=models.SlugField(),
        ),
    ]