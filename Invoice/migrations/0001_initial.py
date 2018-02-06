# Generated by Django 2.0 on 2018-01-26 22:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Cart', '0003_auto_20180125_2215'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_id', models.CharField(max_length=40, unique=True)),
                ('shipping', models.DecimalField(decimal_places=2, default=9.5, max_digits=5)),
                ('total', models.DecimalField(decimal_places=3, default=0.0, max_digits=12)),
                ('status', models.CharField(choices=[('CREATED', 'Created'), ('SHIPPED', 'Shipped'), ('DELIVERED', 'Delivered'), ('CANCLED', 'Cancel')], max_length=12)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Cart.Cart')),
            ],
        ),
    ]