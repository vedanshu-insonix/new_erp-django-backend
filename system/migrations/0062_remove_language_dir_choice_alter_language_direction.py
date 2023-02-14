# Generated by Django 4.0 on 2023-02-14 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0061_alter_configuration_editable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='language',
            name='dir_choice',
        ),
        migrations.AlterField(
            model_name='language',
            name='direction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.choice'),
        ),
    ]
