# Generated by Django 4.2 on 2023-08-10 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile',
            name='city',
            field=models.CharField(default='lahore', max_length=1000),
        ),
    ]
