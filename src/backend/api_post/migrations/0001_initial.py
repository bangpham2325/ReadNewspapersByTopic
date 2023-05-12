# Generated by Django 3.2.8 on 2023-05-12 16:08

import api_post.models.post
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(default='', max_length=255)),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'category',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Contents',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.TextField(blank=True, max_length=255)),
                ('paragraph', models.JSONField(blank=True)),
                ('description_img', models.TextField(blank=True)),
                ('image', models.CharField(blank=True, max_length=255)),
                ('index', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'contents',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('keyword', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'db_table': 'keyword',
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(default='', max_length=255)),
                ('domain', models.CharField(blank=True, max_length=255, unique=True)),
            ],
            options={
                'db_table': 'source',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.TextField(blank=True, max_length=255)),
                ('slug', models.SlugField(null=True, unique=True)),
                ('thumbnail', models.FileField(blank=True, null=True, upload_to=api_post.models.post.upload_path)),
                ('likes', models.IntegerField(default=0)),
                ('publish_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.CharField(blank=True, max_length=255)),
                ('summary', models.CharField(blank=True, max_length=255)),
                ('status', models.CharField(choices=[('DRAFT', 'DRAFT'), ('PUBLISHED', 'PUBLISHED')], default='DRAFT', max_length=50)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='api_post.category')),
            ],
            options={
                'db_table': 'posts',
                'ordering': ['-created_at'],
            },
        ),
    ]