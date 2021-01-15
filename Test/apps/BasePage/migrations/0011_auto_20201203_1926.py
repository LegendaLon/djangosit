# Generated by Django 3.1 on 2020-12-03 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BasePage', '0010_auto_20201124_1959'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commentinnews',
            options={'ordering': ['-date'], 'verbose_name': 'Коментарий', 'verbose_name_plural': 'Коментарии'},
        ),
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ['-date'], 'verbose_name': 'Новость', 'verbose_name_plural': 'Новости'},
        ),
        migrations.RenameField(
            model_name='commentinnews',
            old_name='time',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='news',
            old_name='time',
            new_name='date',
        ),
        migrations.AlterField(
            model_name='commentinnews',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='BasePage.news'),
        ),
    ]
