# Generated by Django 3.1.1 on 2021-08-12 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_inventoryitem_transaction_transactionlineitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_num',
            field=models.TextField(blank=True, null=True),
        ),
    ]
