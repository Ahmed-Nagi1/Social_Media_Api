# Generated by Django 5.1.1 on 2024-09-17 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_alter_reaction_reaction_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='comments_count',
        ),
    ]
