# Generated by Django 3.1 on 2020-11-21 13:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('BasePage', '0004_auto_20201121_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentinnews',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='commentinnews',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='BasePage.news'),
        ),
    ]
