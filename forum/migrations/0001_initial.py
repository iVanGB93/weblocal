# Generated by Django 3.0.5 on 2021-06-08 19:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import forum.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Publicacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tema', models.CharField(choices=[('Noticia', 'Noticia'), ('Internet', 'Internet'), ('JovenClub', 'JovenClub'), ('Emby', 'Emby'), ('FileZilla', 'FileZilla'), ('QbaRed', 'QbaRed')], max_length=15)),
                ('titulo', models.CharField(max_length=60)),
                ('contenido', models.TextField()),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('online', models.BooleanField(default=False)),
                ('visitas', models.PositiveIntegerField(default=0)),
                ('imagen1', models.ImageField(default='defaultForum.png', upload_to=forum.models.upload_to, verbose_name='Imagen1')),
                ('imagen2', models.ImageField(default='defaultForum.png', upload_to=forum.models.upload_to, verbose_name='Imagen2')),
                ('imagen3', models.ImageField(default='defaultForum.png', upload_to=forum.models.upload_to, verbose_name='Imagen3')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
