# Generated by Django 5.0 on 2023-12-15 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0006_post_file_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.CharField(default='admin', max_length=10),
        ),
    ]
