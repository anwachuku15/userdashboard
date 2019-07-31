# Generated by Django 2.0 on 2019-07-31 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_auto_20190731_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='myapp.User'),
            preserve_default=False,
        ),
    ]
