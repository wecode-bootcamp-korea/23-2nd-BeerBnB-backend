# Generated by Django 3.2.5 on 2021-08-20 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='grade',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
