# Generated by Django 2.0 on 2019-07-20 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20190710_2200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='likes',
        ),
    ]
