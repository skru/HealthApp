# Generated by Django 3.0.3 on 2020-04-17 10:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='chat_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
