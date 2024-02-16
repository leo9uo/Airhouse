# Generated by Django 5.0.1 on 2024-02-16 02:20

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airhouse', '0004_inventoryitem_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_no', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('recipient', models.CharField(max_length=255)),
                ('order_date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('new', 'New'), ('processing', 'Processing'), ('shipped', 'Shipped'), ('in_transit', 'In Transit'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='new', max_length=20)),
                ('payment', models.CharField(choices=[('paid', 'Paid'), ('not_paid', 'Not Paid')], default='not_paid', max_length=10)),
                ('order_source', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('inventory_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airhouse.inventoryitem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airhouse.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='skus_ordered',
            field=models.ManyToManyField(through='airhouse.OrderItem', to='airhouse.inventoryitem'),
        ),
    ]
