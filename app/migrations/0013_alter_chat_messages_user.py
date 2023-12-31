# Generated by Django 4.2 on 2023-08-20 10:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0012_chat_messages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat_messages',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_chat', to=settings.AUTH_USER_MODEL),
        ),
    ]
