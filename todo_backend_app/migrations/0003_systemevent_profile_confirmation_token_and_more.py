# Generated by Django 4.1 on 2023-02-03 07:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('todo_backend_app', '0002_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemEvent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id записи')),
                ('event_id', models.UUIDField(verbose_name='id события')),
                ('topic', models.CharField(db_index=True, max_length=255, verbose_name='Топик события')),
                ('payload', models.JSONField(db_index=True, verbose_name='Содержание события')),
                ('published_date', models.DateTimeField(null=True, verbose_name='Дата публикации')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')),
                ('version', models.PositiveIntegerField(default=0, verbose_name='Версия')),
            ],
            options={
                'verbose_name': 'Событие',
                'verbose_name_plural': 'События',
                'db_table': 'todo_backend_system_event',
                'ordering': ('created_date',),
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='confirmation_token',
            field=models.UUIDField(db_index=True, default=None, null=True, verbose_name='Токен для подтверждения аккаунта'),
        ),
        migrations.AddField(
            model_name='profile',
            name='confirmed_date',
            field=models.DateTimeField(db_index=True, default=None, null=True, verbose_name='Дата подтверждения аккаунта'),
        ),
    ]