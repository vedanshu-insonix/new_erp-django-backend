# Generated by Django 4.0 on 2023-02-10 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0031_alter_configuration_editable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='language',
            name='date_format',
        ),
        migrations.RemoveField(
            model_name='language',
            name='decimal_places',
        ),
        migrations.RemoveField(
            model_name='language',
            name='fraction_separator',
        ),
        migrations.RemoveField(
            model_name='language',
            name='symbol_position',
        ),
        migrations.RemoveField(
            model_name='language',
            name='thousands_separator',
        ),
        migrations.RemoveField(
            model_name='language',
            name='time_format',
        ),
        migrations.AddField(
            model_name='language',
            name='code',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AddField(
            model_name='language',
            name='dir_choice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.choice'),
        ),
        migrations.AddField(
            model_name='language',
            name='direction',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='language',
            name='native_Translation',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
