# Generated by Django 4.0 on 2023-02-23 06:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0074_translationicons'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translationchoice',
            name='translation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.translation'),
        ),
        migrations.AlterField(
            model_name='translationcolumn',
            name='column',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.column'),
        ),
        migrations.AlterField(
            model_name='translationcolumn',
            name='translation',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.translation'),
        ),
        migrations.AlterField(
            model_name='translationmenu',
            name='translation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.translation'),
        ),
        migrations.AlterField(
            model_name='translationstage',
            name='stage',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.stage'),
        ),
        migrations.AlterField(
            model_name='translationstage',
            name='translation',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.translation'),
        ),
    ]
