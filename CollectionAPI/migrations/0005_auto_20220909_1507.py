# Generated by Django 2.2.5 on 2022-09-09 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CollectionAPI', '0004_collection'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='description',
            field=models.TextField(default='NA'),
        ),
        migrations.AddField(
            model_name='collection',
            name='title',
            field=models.CharField(default='NA', max_length=1000),
        ),
    ]
