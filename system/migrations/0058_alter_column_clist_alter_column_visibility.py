# Generated by Django 4.0 on 2023-02-13 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0057_remove_list_category_remove_list_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='clist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.list'),
        ),
        migrations.AlterField(
            model_name='column',
            name='visibility',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.choice'),
        ),
    ]
