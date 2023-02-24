# Generated by Django 4.0 on 2023-02-20 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disbursment',
            fields=[
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('id', models.CharField(editable=False, max_length=255, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=30)),
                ('disbursment_for', models.CharField(blank=True, max_length=100, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('1', 'Closed'), ('2', 'Normal'), ('3', 'Warning'), ('4', 'Urgent')], max_length=255, null=True)),
                ('stage_started', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Manufacturingorderlines',
            fields=[
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('id', models.CharField(editable=False, max_length=255, primary_key=True, serialize=False)),
                ('quantity', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Manufacturingorders',
            fields=[
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('id', models.CharField(editable=False, max_length=255, primary_key=True, serialize=False)),
                ('stage_started', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('id', models.CharField(editable=False, max_length=255, primary_key=True, serialize=False)),
                ('purchase_order_id', models.CharField(max_length=10, unique=True)),
                ('contact_first', models.CharField(blank=True, max_length=255, null=True)),
                ('contact_last', models.CharField(blank=True, max_length=255, null=True)),
                ('contact_telephone', models.CharField(blank=True, max_length=255, null=True)),
                ('contact_email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Email')),
                ('purchasing_first', models.CharField(blank=True, max_length=255, null=True)),
                ('purchasing_last', models.CharField(blank=True, max_length=255, null=True)),
                ('purchasing_company', models.CharField(blank=True, max_length=255, null=True)),
                ('purchasing_address_1', models.CharField(blank=True, max_length=255, null=True)),
                ('purchasing_address_2', models.CharField(blank=True, max_length=255, null=True)),
                ('purchasing_address_3', models.CharField(blank=True, max_length=255, null=True)),
                ('purchasing_city', models.CharField(blank=True, max_length=255, null=True)),
                ('purchasing_state', models.CharField(blank=True, max_length=255, null=True)),
                ('purchasing_postal_code', models.CharField(blank=True, max_length=255, null=True)),
                ('purchasing_country', models.CharField(blank=True, max_length=255, null=True)),
                ('purchasing_telephone', models.CharField(blank=True, max_length=255, null=True)),
                ('purchasing_email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Email')),
                ('purchasing_note', models.TextField(blank=True, null=True)),
                ('shipping_first', models.CharField(blank=True, max_length=255, null=True)),
                ('shipping_last', models.CharField(blank=True, max_length=255, null=True)),
                ('shipping_company', models.CharField(blank=True, max_length=255, null=True)),
                ('shipping_address_1', models.CharField(blank=True, max_length=255, null=True)),
                ('shipping_address_2', models.CharField(blank=True, max_length=255, null=True)),
                ('shipping_address_3', models.CharField(blank=True, max_length=255, null=True)),
                ('shipping_city', models.CharField(blank=True, max_length=255, null=True)),
                ('shipping_state', models.CharField(blank=True, max_length=255, null=True)),
                ('shipping_postal_code', models.CharField(blank=True, max_length=255, null=True)),
                ('shipping_country', models.CharField(blank=True, max_length=255, null=True)),
                ('shipping_telephone', models.CharField(blank=True, max_length=255, null=True)),
                ('shipping_email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Email')),
                ('shipping_note', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('reference', models.CharField(blank=True, max_length=255, null=True)),
                ('shipping_terms_choices', models.CharField(blank=True, choices=[('1', 'Prepaid/Prepay'), ('2', 'Add/Collect')], max_length=1, null=True)),
                ('Priority', models.CharField(blank=True, max_length=255, null=True)),
                ('stage_started', models.DateTimeField(auto_now_add=True)),
                ('status_choices_id', models.CharField(blank=True, choices=[('1', 'Closed'), ('2', 'Normal'), ('3', 'Warning'), ('4', 'Urgent')], max_length=1, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PurchaseOrderLines',
            fields=[
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('id', models.CharField(editable=False, max_length=255, primary_key=True, serialize=False)),
                ('vendor_stock_number', models.CharField(blank=True, max_length=255, null=True)),
                ('vendor_product_name', models.CharField(blank=True, max_length=255, null=True)),
                ('vendor_product_description', models.TextField(blank=True, null=True)),
                ('vendor_list_price', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=30)),
                ('vendor_multiplier', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=30)),
                ('ordered', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=30)),
                ('canceled', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=30)),
                ('confirmed', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=30)),
                ('shipped', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=30)),
                ('invoiced', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=30)),
                ('via_choice', models.CharField(blank=True, max_length=255, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('sequence', models.IntegerField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('product', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
