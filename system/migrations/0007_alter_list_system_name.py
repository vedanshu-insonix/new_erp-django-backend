# Generated by Django 4.0 on 2023-01-31 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0006_alter_listicon_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='system_name',
            field=models.CharField(blank=True, default=1, max_length=255),
            preserve_default=False,
        ),
    ]
