# Generated by Django 3.2.4 on 2021-06-24 09:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trafficsign',
            old_name='car',
            new_name='image',
        ),
    ]
