# Generated by Django 3.2.8 on 2023-06-21 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_post', '0006_alter_posts_status'),
        ('api_interaction', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_bookmark', to='api_post.posts'),
        ),
    ]
