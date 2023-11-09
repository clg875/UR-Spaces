# Generated by Django 4.2.7 on 2023-11-09 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_remove_posts_post_sub_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='Post_ID',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='com_count',
        ),
        migrations.AddField(
            model_name='posts',
            name='comments',
            field=models.ManyToManyField(blank=True, to='myapp.comment'),
        ),
    ]
