# Generated by Django 4.2.7 on 2023-11-08 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_posts_subforum_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='SubForum_ID',
        ),
        migrations.DeleteModel(
            name='SubForums',
        ),
    ]