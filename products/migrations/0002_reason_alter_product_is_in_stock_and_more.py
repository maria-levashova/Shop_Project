# Generated by Django 5.0.6 on 2024-07-03 05:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Title')),
            ],
            options={
                'verbose_name': 'Reason',
                'verbose_name_plural': 'Reasons',
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='is_in_stock',
            field=models.BooleanField(default=True, verbose_name='is in stock'),
        ),
        migrations.AlterField(
            model_name='producttag',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_tag', to='products.product', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='producttag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags_of_products', to='products.tag', verbose_name='Tag'),
        ),
        migrations.CreateModel(
            name='ProductReason',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_reason', to='products.product', verbose_name='Product')),
                ('reason', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reasons_of_products', to='products.reason', verbose_name='Tag')),
            ],
            options={
                'verbose_name': 'Product Reason',
                'verbose_name_plural': 'Product Reasons',
            },
        ),
    ]
