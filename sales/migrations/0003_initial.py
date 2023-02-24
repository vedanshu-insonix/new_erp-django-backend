# Generated by Django 4.0 on 2023-02-20 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sales', '0002_initial'),
        ('system', '0001_initial'),
        ('warehouse', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorproducts',
            name='uom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='warehouse.uom'),
        ),
        migrations.AddField(
            model_name='vendorprices',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='vendorprices',
            name='stage_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.stage'),
        ),
        migrations.AddField(
            model_name='vendorprices',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.vendors'),
        ),
        migrations.AddField(
            model_name='vendorprices',
            name='vendor_product_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.vendorproducts'),
        ),
        migrations.AddField(
            model_name='vendoraddress',
            name='address',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.addresses'),
        ),
        migrations.AddField(
            model_name='vendoraddress',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='vendoraddress',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.vendors'),
        ),
        migrations.AddField(
            model_name='salesreturns',
            name='billing_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_billing_address', to='sales.addresses'),
        ),
        migrations.AddField(
            model_name='salesreturns',
            name='billing_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_blling_country', to='system.country'),
        ),
        migrations.AddField(
            model_name='salesreturns',
            name='billing_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_billing_state', to='system.state'),
        ),
        migrations.AddField(
            model_name='salesreturns',
            name='contact_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_contact_address', to='sales.addresses'),
        ),
        migrations.AddField(
            model_name='salesreturns',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='salesreturns',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.currency'),
        ),
        migrations.AddField(
            model_name='salesreturns',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.customers'),
        ),
        migrations.AddField(
            model_name='salesreturns',
            name='invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.salesinvoices'),
        ),
        migrations.AddField(
            model_name='salesreturns',
            name='return_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_return_address', to='sales.addresses'),
        ),
        migrations.AddField(
            model_name='salesreturns',
            name='return_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_return_country', to='system.country'),
        ),
        migrations.AddField(
            model_name='salesreturns',
            name='return_stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.stage'),
        ),
        migrations.AddField(
            model_name='salesreturns',
            name='return_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_return_state', to='system.state'),
        ),
        migrations.AddField(
            model_name='salesreturnlines',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='salesreturnlines',
            name='stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.stage'),
        ),
        migrations.AddField(
            model_name='salesquotations',
            name='accepted_currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.currency'),
        ),
        migrations.AddField(
            model_name='salesquotations',
            name='billing_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_billing_address', to='sales.addresses'),
        ),
        migrations.AddField(
            model_name='salesquotations',
            name='billing_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_blling_country', to='system.country'),
        ),
        migrations.AddField(
            model_name='salesquotations',
            name='billing_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_billing_state', to='system.state'),
        ),
        migrations.AddField(
            model_name='salesquotations',
            name='contact_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_contact_address', to='sales.addresses'),
        ),
        migrations.AddField(
            model_name='salesquotations',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='salesquotations',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.customers'),
        ),
        migrations.AddField(
            model_name='salesquotations',
            name='quotation_stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.stage'),
        ),
        migrations.AddField(
            model_name='salesquotations',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_shipping_address', to='sales.addresses'),
        ),
        migrations.AddField(
            model_name='salesquotations',
            name='shipping_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_shipping_country', to='system.country'),
        ),
        migrations.AddField(
            model_name='salesquotations',
            name='shipping_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_shipping_state', to='system.state'),
        ),
        migrations.AddField(
            model_name='salesquotationlines',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='salesquotationlines',
            name='quotation_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.currency'),
        ),
        migrations.AddField(
            model_name='salesquotationlines',
            name='route',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='warehouse.routes'),
        ),
        migrations.AddField(
            model_name='salesquotationlines',
            name='stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.stage'),
        ),
        migrations.AddField(
            model_name='salespricelists',
            name='category_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.category'),
        ),
        migrations.AddField(
            model_name='salespricelists',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='salespricelists',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.customers'),
        ),
        migrations.AddField(
            model_name='salesorders',
            name='accepted_currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.currency'),
        ),
        migrations.AddField(
            model_name='salesorders',
            name='billing_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_billing_address', to='sales.addresses'),
        ),
        migrations.AddField(
            model_name='salesorders',
            name='billing_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_blling_country', to='system.country'),
        ),
        migrations.AddField(
            model_name='salesorders',
            name='billing_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_billing_state', to='system.state'),
        ),
        migrations.AddField(
            model_name='salesorders',
            name='contact_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_contact_address', to='sales.addresses'),
        ),
        migrations.AddField(
            model_name='salesorders',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='salesorders',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.customers'),
        ),
        migrations.AddField(
            model_name='salesorders',
            name='order_stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.stage'),
        ),
        migrations.AddField(
            model_name='salesorders',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_shipping_address', to='sales.addresses'),
        ),
        migrations.AddField(
            model_name='salesorders',
            name='shipping_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_shipping_country', to='system.country'),
        ),
        migrations.AddField(
            model_name='salesorders',
            name='shipping_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_shipping_state', to='system.state'),
        ),
        migrations.AddField(
            model_name='salesorderlines',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='salesorderlines',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales.salesorders'),
        ),
        migrations.AddField(
            model_name='salesorderlines',
            name='orderline_stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.stage'),
        ),
        migrations.AddField(
            model_name='salesorderlines',
            name='route',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='warehouse.routes'),
        ),
        migrations.AddField(
            model_name='salesorderlines',
            name='uom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='warehouse.uom'),
        ),
        migrations.AddField(
            model_name='salesinvoices',
            name='billing_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_billing_address', to='sales.addresses'),
        ),
        migrations.AddField(
            model_name='salesinvoices',
            name='billing_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_blling_country', to='system.country'),
        ),
        migrations.AddField(
            model_name='salesinvoices',
            name='billing_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_billing_state', to='system.state'),
        ),
        migrations.AddField(
            model_name='salesinvoices',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='salesinvoices',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.currency'),
        ),
        migrations.AddField(
            model_name='salesinvoices',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.customers'),
        ),
        migrations.AddField(
            model_name='salesinvoices',
            name='sales_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.salesorders'),
        ),
        migrations.AddField(
            model_name='salesinvoices',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_shipping_address', to='sales.addresses'),
        ),
        migrations.AddField(
            model_name='salesinvoices',
            name='shipping_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_shipping_country', to='system.country'),
        ),
        migrations.AddField(
            model_name='salesinvoices',
            name='shipping_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_shipping_state', to='system.state'),
        ),
        migrations.AddField(
            model_name='salesinvoices',
            name='stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.stage'),
        ),
        migrations.AddField(
            model_name='salescredits',
            name='accepted_currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.currency'),
        ),
        migrations.AddField(
            model_name='salescredits',
            name='billing_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_billing_address', to='sales.addresses'),
        ),
        migrations.AddField(
            model_name='salescredits',
            name='billing_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_blling_country', to='system.country'),
        ),
        migrations.AddField(
            model_name='salescredits',
            name='billing_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_billing_state', to='system.state'),
        ),
        migrations.AddField(
            model_name='salescredits',
            name='contact_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_contact_address', to='sales.addresses'),
        ),
        migrations.AddField(
            model_name='salescredits',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='salescredits',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.customers'),
        ),
        migrations.AddField(
            model_name='salescredits',
            name='invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.salesinvoices'),
        ),
        migrations.AddField(
            model_name='salescredits',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_shipping_address', to='sales.addresses'),
        ),
        migrations.AddField(
            model_name='salescredits',
            name='shipping_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_shipping_country', to='system.country'),
        ),
        migrations.AddField(
            model_name='salescredits',
            name='shipping_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_shipping_state', to='system.state'),
        ),
        migrations.AddField(
            model_name='salescredits',
            name='stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.stage'),
        ),
        migrations.AddField(
            model_name='receipts',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='receipts',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.currency'),
        ),
        migrations.AddField(
            model_name='receipts',
            name='sales_invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales.salesinvoices'),
        ),
        migrations.AddField(
            model_name='receipts',
            name='stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.stage'),
        ),
        migrations.AddField(
            model_name='nmfc',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='customsclassifications',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='customers',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='customers',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer_currency', to='system.currency'),
        ),
        migrations.AddField(
            model_name='customers',
            name='customer_stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.stage'),
        ),
        migrations.AddField(
            model_name='customers',
            name='parent_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales.customers'),
        ),
        migrations.AddField(
            model_name='customeraddress',
            name='address',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.addresses'),
        ),
        migrations.AddField(
            model_name='customeraddress',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='customeraddress',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.customers'),
        ),
        migrations.AddField(
            model_name='carts',
            name='billing_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_billing_address', to='sales.addresses'),
        ),
        migrations.AddField(
            model_name='carts',
            name='contact_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_contact_address', to='sales.addresses'),
        ),
        migrations.AddField(
            model_name='carts',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='carts',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.currency'),
        ),
        migrations.AddField(
            model_name='carts',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.customers'),
        ),
        migrations.AddField(
            model_name='carts',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_shipping_address', to='sales.addresses'),
        ),
        migrations.AddField(
            model_name='carts',
            name='stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.stage'),
        ),
        migrations.AddField(
            model_name='cartlines',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.carts'),
        ),
        migrations.AddField(
            model_name='cartlines',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='cartlines',
            name='stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.stage'),
        ),
        migrations.AddField(
            model_name='addresstag',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.addresses'),
        ),
        migrations.AddField(
            model_name='addresstag',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='addresstag',
            name='tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='system.tag'),
        ),
        migrations.AddField(
            model_name='addresses',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.country'),
        ),
        migrations.AddField(
            model_name='addresses',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to='auth.user'),
        ),
        migrations.AddField(
            model_name='addresses',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.language'),
        ),
        migrations.AddField(
            model_name='addresses',
            name='stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.stage'),
        ),
        migrations.AddField(
            model_name='addresses',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='system.state'),
        ),
    ]
