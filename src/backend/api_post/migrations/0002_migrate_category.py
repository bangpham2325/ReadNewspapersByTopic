# Generated by Django 3.2.8 on 2022-02-16 06:05

from django.db import migrations


from django.db import migrations

import json


def initial_category(apps, schema_editor):

    category_model = apps.get_model("api_post", "Category")

    category_data = json.load(open('api_post/constants/category.json', encoding="utf8"))

    categories = []

    for category in category_data:
            category_dict = category_model(id=category['id'], title=category['title'], description=category['description'])
            categories.append(category_dict)

    category_model.objects.bulk_create(categories)


def delete_all_category(apps, schema_editor):
    category_model = apps.get_model("api_post", "Category")
    category_model.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('api_post', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(initial_category, delete_all_category)
    ]