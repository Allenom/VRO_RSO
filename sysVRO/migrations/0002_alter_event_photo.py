# Generated by Django 4.1.7 on 2023-03-03 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sysVRO', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='event/img'),
        ),
    ]