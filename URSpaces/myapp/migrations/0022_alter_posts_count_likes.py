# Generated by Django 4.2.7 on 2023-11-09 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0021_alter_posts_count_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='count_likes',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
