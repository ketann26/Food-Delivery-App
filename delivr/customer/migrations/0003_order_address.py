# Generated by Django 4.2.7 on 2023-11-05 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_order_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.TextField(null=True),
        ),
    ]
