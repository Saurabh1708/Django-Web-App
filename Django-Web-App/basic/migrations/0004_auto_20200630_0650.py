# Generated by Django 3.0.3 on 2020-06-30 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0003_cart_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
