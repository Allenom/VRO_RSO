# Generated by Django 4.1.7 on 2023-03-24 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sysVRO', '0018_remove_profile_position'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='detachment',
            new_name='detachment_member',
        ),
    ]
