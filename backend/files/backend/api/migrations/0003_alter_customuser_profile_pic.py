# Generated by Django 4.2.7 on 2024-01-15 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_customuser_mobile_customuser_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_pic',
            field=models.FileField(blank=True, default='profilepic/default.jpg', null=True, upload_to='profilepic/'),
        ),
    ]