# Generated by Django 3.0.5 on 2021-07-13 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sync', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='estadoconexion',
            name='sync',
            field=models.BooleanField(default=False),
        ),
    ]