# Generated by Django 4.2.7 on 2023-11-08 05:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_remove_posts_subforum_id_delete_subforums'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubForums',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='posts',
            name='SubForum_ID',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.subforums'),
        ),
    ]
