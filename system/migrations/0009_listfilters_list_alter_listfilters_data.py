# Generated by Django 4.0 on 2023-02-01 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0008_remove_list_data_filter_remove_list_data_sort'),
    ]

    operations = [
        migrations.AddField(
            model_name='listfilters',
            name='list',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='system.list'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='listfilters',
            name='data',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='system.data'),
            preserve_default=False,
        ),
    ]
