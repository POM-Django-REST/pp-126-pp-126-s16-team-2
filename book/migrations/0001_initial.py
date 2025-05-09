# Generated by Django 4.1 on 2025-04-03 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('name', models.CharField(blank=True, max_length=128)),
                ('description', models.TextField(blank=True, max_length=256)),
                ('count', models.IntegerField(default=10)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('borrowed_books', models.IntegerField(default=0)),
            ],
            options={
                'permissions': [('can_view_books', 'Can view books'), ('can_edit_books', 'Can edit books')],
            },
        ),
        migrations.CreateModel(
            name='BorrowedBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrow_date', models.DateField(auto_now_add=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='LibraryMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrowed_books', models.ManyToManyField(related_name='borrowed_by_members', through='book.BorrowedBook', to='book.book')),
            ],
        ),
    ]
