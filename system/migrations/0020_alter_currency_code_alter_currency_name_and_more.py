# Generated by Django 4.0 on 2023-02-07 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0019_alter_currency_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='code',
            field=models.CharField(blank=True, default=1, max_length=3),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='currency',
            name='name',
            field=models.CharField(blank=True, default=1, max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='currency',
            name='symbol',
            field=models.CharField(blank=True, default=1, max_length=10),
            preserve_default=False,
        ),
    ]
