# Generated by Django 3.2.3 on 2021-05-30 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hexocean', '0012_link_uuid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='link',
            old_name='seconds_to_exp',
            new_name='seconds',
        ),
    ]
