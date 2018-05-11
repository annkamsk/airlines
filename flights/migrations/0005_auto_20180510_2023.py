# Generated by Django 2.0.4 on 2018-05-10 18:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0004_auto_20180507_2224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flight',
            name='landingDate',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='startingDate',
        ),
        migrations.AlterField(
            model_name='flight',
            name='landingTime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='flight',
            name='startingTime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]