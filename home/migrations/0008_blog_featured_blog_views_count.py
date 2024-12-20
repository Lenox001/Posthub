# Generated by Django 5.1.2 on 2024-12-09 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_reply_replied_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='blog',
            name='views_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
