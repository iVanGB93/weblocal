# Generated by Django 3.0.5 on 2021-04-28 20:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sorteo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SorteoDetalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('activo', models.BooleanField(default=False)),
            ],
        ),
    ]