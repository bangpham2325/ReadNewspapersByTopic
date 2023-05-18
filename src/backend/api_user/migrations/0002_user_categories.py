# Generated by Django 3.2.8 on 2023-05-17 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_post', '0003_posts_views'),
        ('api_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='categories',
            field=models.ManyToManyField(blank=True, null=True, related_name='user', to='api_post.Category'),
        ),
    ]
