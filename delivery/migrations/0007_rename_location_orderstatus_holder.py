# Generated by Django 3.2.4 on 2021-06-20 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0006_alter_orderstatus_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderstatus',
            old_name='location',
            new_name='holder',
        ),
    ]