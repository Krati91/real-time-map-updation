# Generated by Django 3.2.4 on 2021-06-16 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(to='delivery.Product'),
        ),
    ]
