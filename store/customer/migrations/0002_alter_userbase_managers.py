# Generated by Django 3.2.6 on 2021-09-02 22:14

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='userbase',
            managers=[
                ('objects1', django.db.models.manager.Manager()),
            ],
        ),
    ]