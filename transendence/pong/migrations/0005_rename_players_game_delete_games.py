# Generated by Django 4.2.7 on 2023-11-30 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pong', '0004_games_topic'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Players',
            new_name='Game',
        ),
        migrations.DeleteModel(
            name='Games',
        ),
    ]
