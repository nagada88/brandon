# Generated by Django 4.0.3 on 2023-04-08 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_brandon_photography', '0004_blogpost_created_at_blogpost_extract_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='title',
            field=models.CharField(default='egy cim', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='user',
            field=models.CharField(default='Nagy Ádám', max_length=200),
        ),
    ]
