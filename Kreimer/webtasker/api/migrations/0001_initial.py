# Generated by Django 4.2.5 on 2023-09-13 20:18

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
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='default_for_now', max_length=50)),
                ('description', models.TextField(default='default_for_now', max_length=200)),
                ('invite_code', models.CharField(max_length=8, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Host', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='Members', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='default_for_now', max_length=50)),
                ('number', models.IntegerField()),
                ('id_board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.board')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='default_for_now', max_length=50)),
                ('body', models.TextField(default='default_for_now', max_length=200)),
                ('color', models.IntegerField()),
                ('priority', models.IntegerField()),
                ('finish_by', models.DateTimeField()),
                ('id_column', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.column')),
                ('taken_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
