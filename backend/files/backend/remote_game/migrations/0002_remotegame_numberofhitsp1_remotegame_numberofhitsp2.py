# Generated by Django 4.2.7 on 2024-01-15 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remote_game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='remotegame',
            name='numberofHitsP1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='remotegame',
            name='numberofHitsP2',
            field=models.IntegerField(default=0),
        ),
    ]
