# Generated by Django 5.1.1 on 2024-10-16 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
