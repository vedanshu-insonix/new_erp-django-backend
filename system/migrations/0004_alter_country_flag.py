# Generated by Django 4.0 on 2023-03-15 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0003_remove_country_country_country_country_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='flag',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to='flag/'),
        ),
    ]
