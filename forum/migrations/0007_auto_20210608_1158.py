# Generated by Django 3.0.5 on 2021-06-08 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_auto_20210608_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicacion',
            name='vistas',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
