# Generated by Django 4.2.7 on 2023-11-13 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0026_comment_likes_posts_likes'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Like',
        ),
    ]
