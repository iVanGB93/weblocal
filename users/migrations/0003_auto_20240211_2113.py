# Generated by Django 3.0.5 on 2024-02-12 02:13

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20240201_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='subnet',
            field=models.CharField(default='local_iVan', max_length=50),
        ),
        migrations.AlterField(
            model_name='profile',
            name='imagen',
            field=models.ImageField(default='usuario/defaultUsuario.jpg', upload_to=users.models.upload_to, verbose_name='Image'),
        ),
    ]
