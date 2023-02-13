# Generated by Django 4.0 on 2023-02-07 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0014_selectors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='editable',
        ),
        migrations.AlterField(
            model_name='choice',
            name='deafult',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='choice',
            name='selector',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.selectors'),
        ),
    ]
