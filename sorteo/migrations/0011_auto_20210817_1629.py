# Generated by Django 3.0.5 on 2021-08-17 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sorteo', '0010_auto_20210710_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='sorteo',
            name='sync',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='sorteo',
            name='mes',
            field=models.CharField(default=8, max_length=10),
        ),
        migrations.AlterField(
            model_name='sorteodetalle',
            name='mes',
            field=models.CharField(default=8, max_length=10),
        ),
    ]