# Generated by Django 5.1.3 on 2024-11-12 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_duck_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="duck",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
