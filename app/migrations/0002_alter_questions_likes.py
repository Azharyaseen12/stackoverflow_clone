# Generated by Django 4.2 on 2023-08-03 18:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='likes',
            field=models.ManyToManyField(related_name='like', to=settings.AUTH_USER_MODEL),
        ),
    ]
