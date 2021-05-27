# Generated by Django 3.1.7 on 2021-05-24 06:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('chat_id', models.AutoField(primary_key=True, serialize=False)),
                ('account1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account1', to=settings.AUTH_USER_MODEL)),
                ('account2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('message_id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('time', models.DateTimeField(db_index=True)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chat')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('parentMessage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='chat.message')),
            ],
        ),
    ]
