# Generated by Django 4.2.7 on 2024-01-11 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_statistics_games_played_statistics_mmr_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistics',
            name='games_played',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='mmr',
            field=models.IntegerField(default=200),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='ranking',
            field=models.IntegerField(default=0),
        ),
    ]
