# Generated by Django 3.0.5 on 2021-05-07 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sorteo', '0007_sorteo_mes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sorteo',
            name='mes',
            field=models.CharField(default=5, max_length=10),
        ),
        migrations.AlterField(
            model_name='sorteodetalle',
            name='mes',
            field=models.CharField(default=5, max_length=10),
        ),
    ]