# Generated by Django 4.0 on 2023-02-13 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0055_rename_position_column_sequence_remove_column_field_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='column',
            old_name='list',
            new_name='clist',
        ),
    ]
