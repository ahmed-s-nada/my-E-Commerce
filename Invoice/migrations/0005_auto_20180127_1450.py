# Generated by Django 2.0 on 2018-01-27 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Invoice', '0004_auto_20180127_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cart.Cart'),
        ),
    ]
