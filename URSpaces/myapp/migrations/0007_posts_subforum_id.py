# Generated by Django 4.2.7 on 2023-11-08 05:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_remove_posts_subforum_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='SubForum_ID',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.subforums'),
            preserve_default=False,
        ),
    ]
