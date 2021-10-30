# Generated by Django 3.2.7 on 2021-10-27 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='genre',
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(blank=True, to='warehouse.Genre', verbose_name='genre'),
        ),
    ]
