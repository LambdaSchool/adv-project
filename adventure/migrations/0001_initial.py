# Generated by Django 2.1.1 on 2019-08-01 03:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_progress', models.BooleanField(default=False)),
                ('map_columns', models.IntegerField(default=5)),
                ('min_room_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('current_room', models.IntegerField(default=-1)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('game_id', models.IntegerField(default=-1)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='DEFAULT TITLE', max_length=50)),
                ('description', models.CharField(default='DEFAULT DESCRIPTION', max_length=500)),
                ('visited', models.BooleanField(default=False)),
                ('end', models.BooleanField(default=False)),
                ('n', models.IntegerField(default=-1)),
                ('s', models.IntegerField(default=-1)),
                ('e', models.IntegerField(default=-1)),
                ('w', models.IntegerField(default=-1)),
            ],
        ),
    ]
