# Generated by Django 5.1.5 on 2025-01-16 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChatApp', '0003_alter_channel_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
