# Generated by Django 2.0 on 2019-07-31 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_auto_20190731_1224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='postedfor',
        ),
        migrations.RemoveField(
            model_name='message',
            name='user',
        ),
        migrations.AddField(
            model_name='message',
            name='author',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='messagesposted', to='myapp.User'),
            preserve_default=False,
        ),
    ]