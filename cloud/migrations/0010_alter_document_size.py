# Generated by Django 5.0 on 2023-12-19 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0009_remove_post_document_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='size',
            field=models.IntegerField(null=True, verbose_name='file size'),
        ),
    ]
