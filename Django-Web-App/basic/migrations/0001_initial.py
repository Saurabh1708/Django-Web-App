# Generated by Django 3.0.3 on 2020-06-27 17:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=50, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=50, verbose_name='last name')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Cart',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('district', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=256, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name_plural': 'City',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('name', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Country',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('mobile_1', models.CharField(max_length=256)),
                ('mobile_2', models.CharField(max_length=256)),
                ('mobile_3', models.CharField(max_length=256)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.CreateModel(
            name='Pincode',
            fields=[
                ('pincode', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.City')),
            ],
            options={
                'verbose_name_plural': 'Pincode',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=256)),
                ('duration_type', models.DurationField()),
                ('product_description', models.CharField(max_length=256)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tagline', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name_plural': 'Product',
            },
        ),
        migrations.CreateModel(
            name='ProductDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.PositiveIntegerField()),
                ('discount_id', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_published_mobile', models.BooleanField(default=False)),
                ('is_published_web', models.BooleanField(default=True)),
                ('is_published_android', models.BooleanField(default=True)),
                ('is_published_ios', models.BooleanField(default=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.Product')),
            ],
            options={
                'verbose_name_plural': 'Product Details',
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cookie_id', models.CharField(max_length=256)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('no_of_clicks', models.PositiveIntegerField(verbose_name='clicks')),
                ('no_of_pages_viewed', models.PositiveIntegerField(verbose_name='pages viewed')),
            ],
            options={
                'verbose_name_plural': 'Sessions',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.Country')),
            ],
            options={
                'verbose_name_plural': 'State',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=256)),
                ('last_name', models.CharField(max_length=256)),
                ('mobile_1', models.PositiveIntegerField()),
                ('mobile_2', models.PositiveIntegerField()),
                ('mobile_3', models.PositiveIntegerField(null=True)),
                ('email', models.EmailField(max_length=254)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('creation_channel', models.CharField(choices=[('M', 'Mobile'), ('W', 'Web'), ('A', 'Android'), ('iOS', 'iOS')], max_length=20)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Supplier',
            },
        ),
        migrations.CreateModel(
            name='SupplierType',
            fields=[
                ('supplier_type', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Supplier Type',
            },
        ),
        migrations.CreateModel(
            name='SupplierDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('address_1', models.CharField(max_length=256)),
                ('address_2', models.CharField(max_length=256)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('opening_time', models.TimeField()),
                ('closing_time', models.TimeField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.City')),
                ('pincode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.Pincode')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.State')),
                ('supplier_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.Supplier')),
            ],
            options={
                'verbose_name_plural': 'Supplier Details',
            },
        ),
        migrations.AddField(
            model_name='supplier',
            name='supplier_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.SupplierType'),
        ),
        migrations.CreateModel(
            name='ProductListingLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.PositiveIntegerField()),
                ('discount_id', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_published_mobile', models.BooleanField(default=False)),
                ('is_published_web', models.BooleanField(default=True)),
                ('is_published_android', models.BooleanField(default=True)),
                ('is_published_ios', models.BooleanField(default=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.Product')),
                ('supplier_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.Supplier')),
            ],
            options={
                'verbose_name_plural': 'Listing Log',
            },
        ),
        migrations.CreateModel(
            name='ProductDetailsImages',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('image_type', models.CharField(max_length=256)),
                ('is_default_image', models.BooleanField(verbose_name='default image')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product_details_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.ProductDetails')),
            ],
            options={
                'verbose_name_plural': 'Product Details Id',
            },
        ),
        migrations.AddField(
            model_name='productdetails',
            name='supplier_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.Supplier'),
        ),
        migrations.CreateModel(
            name='PricingLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product_details_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.ProductDetails')),
            ],
            options={
                'verbose_name_plural': 'Pricing Log',
            },
        ),
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount_id', models.PositiveIntegerField()),
                ('gst', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.ProductDetails')),
            ],
            options={
                'verbose_name_plural': 'Pricing',
            },
        ),
        migrations.CreateModel(
            name='CustomerDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=20)),
                ('age', models.PositiveIntegerField()),
                ('address_1', models.CharField(max_length=256)),
                ('address_2', models.CharField(max_length=256)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('creation_channel', models.CharField(choices=[('M', 'Mobile'), ('W', 'Web'), ('A', 'Android'), ('iOS', 'iOS')], max_length=20)),
                ('customer_ip', models.CharField(max_length=256)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.City')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.Customer')),
                ('pincode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.Pincode')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.State')),
            ],
            options={
                'verbose_name_plural': 'Customer Details',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.State'),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cart_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.Cart')),
                ('product_details_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.ProductDetails')),
            ],
            options={
                'verbose_name_plural': 'Cart Items',
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='customer_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='basic.Customer'),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('booking_stage', models.CharField(choices=[('C', 'Confirmed'), ('F', 'Failed')], max_length=10)),
                ('booking_datetime', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cart_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.Cart')),
                ('product_details_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.ProductDetails')),
            ],
            options={
                'verbose_name_plural': 'Booking',
            },
        ),
    ]