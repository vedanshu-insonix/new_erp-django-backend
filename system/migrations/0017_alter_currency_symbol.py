# Generated by Django 4.0 on 2023-02-07 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0016_alter_currency_symbol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='symbol',
            field=models.CharField(max_length=5, null=True),
        ),
    ]
