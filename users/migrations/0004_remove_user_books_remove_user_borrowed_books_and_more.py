# Generated by Django 4.1 on 2025-04-05 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='books',
        ),
        migrations.RemoveField(
            model_name='user',
            name='borrowed_books',
        ),
        migrations.RemoveField(
            model_name='user',
            name='returned_books',
        ),
        migrations.RemoveField(
            model_name='user',
            name='viewed_books',
        ),
    ]
