# Generated by Django 4.0 on 2023-03-17 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0006_remove_stage_form_entityaccounts_accounts_formstage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listfilters',
            name='operator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relational_operators', to='system.choice'),
        ),
    ]
