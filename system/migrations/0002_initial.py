# Generated by Django 4.0 on 2023-03-03 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sales', '0003_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('system', '0001_initial'),
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='translationcontainertype',
            name='containerType',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='warehouse.containertypes'),
        ),
        migrations.AddField(
            model_name='translationcontainertype',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='translationcontainertype',
            name='translation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.translation'),
        ),
        migrations.AddField(
            model_name='translationconfiguration',
            name='Configuration',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.configuration'),
        ),
        migrations.AddField(
            model_name='translationconfiguration',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='translationconfiguration',
            name='translation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.translation'),
        ),
        migrations.AddField(
            model_name='translationcolumn',
            name='column',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='system.column'),
        ),
        migrations.AddField(
            model_name='translationcolumn',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='translationcolumn',
            name='translation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='system.translation'),
        ),
        migrations.AddField(
            model_name='translationchoice',
            name='choice',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='system.choice'),
        ),
        migrations.AddField(
            model_name='translationchoice',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='translationchoice',
            name='translation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='system.translation'),
        ),
        migrations.AddField(
            model_name='translationbutton',
            name='button',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='system.button'),
        ),
        migrations.AddField(
            model_name='translationbutton',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='translationbutton',
            name='translation',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='system.translation'),
        ),
        migrations.AddField(
            model_name='translation',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='translation',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.language'),
        ),
        migrations.AddField(
            model_name='translation',
            name='table',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.datatable'),
        ),
        migrations.AddField(
            model_name='tile',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='tile',
            name='list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.list'),
        ),
        migrations.AddField(
            model_name='territories',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='teamuser',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='teamuser',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='system.team'),
        ),
        migrations.AddField(
            model_name='teamuser',
            name='team_responsibility',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.choice'),
        ),
        migrations.AddField(
            model_name='teamuser',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='TeamUser', to='auth.user'),
        ),
        migrations.AddField(
            model_name='teamrole',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='teamrole',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='system.role'),
        ),
        migrations.AddField(
            model_name='teamrole',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='system.team'),
        ),
        migrations.AddField(
            model_name='team',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='team',
            name='stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.stage'),
        ),
        migrations.AddField(
            model_name='team',
            name='team_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.choice'),
        ),
        migrations.AddField(
            model_name='tag',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='state',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='system.country'),
        ),
        migrations.AddField(
            model_name='state',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='stageaction',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='stageaction',
            name='stage',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='system.stage'),
        ),
        migrations.AddField(
            model_name='stage',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='stage',
            name='form',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.form'),
        ),
        migrations.AddField(
            model_name='selectors',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='rules',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='roleterritories',
            name='Territories',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.territories'),
        ),
        migrations.AddField(
            model_name='roleterritories',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='roleterritories',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.role'),
        ),
        migrations.AddField(
            model_name='rolepermissions',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='rolepermissions',
            name='permissions',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.permission'),
        ),
        migrations.AddField(
            model_name='rolepermissions',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.role'),
        ),
        migrations.AddField(
            model_name='rolecategories',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.category'),
        ),
        migrations.AddField(
            model_name='rolecategories',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='rolecategories',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.role'),
        ),
        migrations.AddField(
            model_name='role',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='recordidentifiers',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='permission',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='permission',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.entity'),
        ),
        migrations.AddField(
            model_name='permission',
            name='visibility',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.choice'),
        ),
        migrations.AddField(
            model_name='menu',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='menu',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.entity'),
        ),
        migrations.AddField(
            model_name='menu',
            name='list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.list'),
        ),
        migrations.AddField(
            model_name='menu',
            name='menu_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.choice'),
        ),
        migrations.AddField(
            model_name='listsorts',
            name='column',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.column'),
        ),
        migrations.AddField(
            model_name='listsorts',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='listsorts',
            name='sort_direction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.choice'),
        ),
        migrations.AddField(
            model_name='listicon',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='listicon',
            name='icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.icons'),
        ),
        migrations.AddField(
            model_name='listicon',
            name='list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.list'),
        ),
        migrations.AddField(
            model_name='listfilters',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='listfilters',
            name='data',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.data'),
        ),
        migrations.AddField(
            model_name='listfilters',
            name='list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.list'),
        ),
        migrations.AddField(
            model_name='listfilters',
            name='operator_choice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.choice'),
        ),
        migrations.AddField(
            model_name='list',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='list',
            name='data_source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.datatable'),
        ),
        migrations.AddField(
            model_name='list',
            name='list_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='list_type', to='system.choice'),
        ),
        migrations.AddField(
            model_name='language',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='language',
            name='direction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='language_direction', to='system.choice'),
        ),
        migrations.AddField(
            model_name='icons',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='help',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='help',
            name='form',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.form'),
        ),
        migrations.AddField(
            model_name='help',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.language'),
        ),
        migrations.AddField(
            model_name='formsection',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='formsection',
            name='form',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.form'),
        ),
        migrations.AddField(
            model_name='formlist',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='formlist',
            name='form',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.form'),
        ),
        migrations.AddField(
            model_name='formlist',
            name='list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.list'),
        ),
        migrations.AddField(
            model_name='formicon',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='formicon',
            name='form',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.form'),
        ),
        migrations.AddField(
            model_name='formicon',
            name='icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.icons'),
        ),
        migrations.AddField(
            model_name='formdata',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='formdata',
            name='data',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.data'),
        ),
        migrations.AddField(
            model_name='formdata',
            name='form',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.form'),
        ),
        migrations.AddField(
            model_name='formdata',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.formsection'),
        ),
        migrations.AddField(
            model_name='formdata',
            name='table',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.datatable'),
        ),
        migrations.AddField(
            model_name='formdata',
            name='visibility',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.choice'),
        ),
        migrations.AddField(
            model_name='form',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='entityuser',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='entityuser',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.entity'),
        ),
        migrations.AddField(
            model_name='entityuser',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
        migrations.AddField(
            model_name='entityteam',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='entityteam',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.entity'),
        ),
        migrations.AddField(
            model_name='entityteam',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.team'),
        ),
        migrations.AddField(
            model_name='entityproducts',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='entityproducts',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.entity'),
        ),
        migrations.AddField(
            model_name='entityproducts',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='warehouse.product'),
        ),
        migrations.AddField(
            model_name='entitymenuitem',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='entitymenuitem',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.entity'),
        ),
        migrations.AddField(
            model_name='entitymenuitem',
            name='menu_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.menu'),
        ),
        migrations.AddField(
            model_name='entitylist',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='entitylist',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.entity'),
        ),
        migrations.AddField(
            model_name='entitylist',
            name='list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.list'),
        ),
        migrations.AddField(
            model_name='entityforms',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='entityforms',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.entity'),
        ),
        migrations.AddField(
            model_name='entityforms',
            name='form',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.form'),
        ),
        migrations.AddField(
            model_name='entityaddress',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.addresses'),
        ),
        migrations.AddField(
            model_name='entityaddress',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='entityaddress',
            name='entity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='system.entity'),
        ),
        migrations.AddField(
            model_name='entityaccounts',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='entityaccounts',
            name='entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.entity'),
        ),
        migrations.AddField(
            model_name='entity',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='entity',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.entity'),
        ),
        migrations.AddField(
            model_name='entity',
            name='stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.stage'),
        ),
        migrations.AddField(
            model_name='datatable',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='data',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='data',
            name='data_source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.datatable'),
        ),
        migrations.AddField(
            model_name='currency',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='country',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='country',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.currency'),
        ),
        migrations.AddField(
            model_name='country',
            name='date_format',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='country_date_format', to='system.choice'),
        ),
        migrations.AddField(
            model_name='country',
            name='money_format',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='country_money_format', to='system.choice'),
        ),
        migrations.AddField(
            model_name='country',
            name='symbol_position',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='country_symbol_position', to='system.choice'),
        ),
        migrations.AddField(
            model_name='country',
            name='time_format',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='country_time_format', to='system.choice'),
        ),
        migrations.AddField(
            model_name='configuration',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='communicationaddress',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.addresses'),
        ),
        migrations.AddField(
            model_name='communicationaddress',
            name='communication',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='system.communication'),
        ),
        migrations.AddField(
            model_name='communicationaddress',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='communication',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='communication',
            name='stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.stage'),
        ),
        migrations.AddField(
            model_name='column',
            name='col_list',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.list'),
        ),
        migrations.AddField(
            model_name='column',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='column',
            name='visibility',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.choice'),
        ),
        migrations.AddField(
            model_name='choice',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='choice',
            name='selector',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.selectors'),
        ),
        migrations.AddField(
            model_name='channel',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='category',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='button',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='button',
            name='form',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.form'),
        ),
    ]
