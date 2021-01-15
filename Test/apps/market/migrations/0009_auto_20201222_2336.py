# Generated by Django 3.1 on 2020-12-22 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0008_auto_20201218_0025'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-date'], 'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterField(
            model_name='order',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание к заказу'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('В ожидании', 'В ожидании'), ('Задерживаеться', 'Задерживаеться'), ('Принят', 'Принят'), ('Завершено', 'Завершено'), ('Отклонено', 'Отклонено')], default='В ожидании', max_length=60, verbose_name='Статус'),
        ),
    ]