# Generated by Django 5.1.1 on 2024-11-14 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_post_likes_alter_like_post_alter_like_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='frecuencia_base',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True, verbose_name='Frecuencia base (GHz)'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='frecuencia_boost',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True, verbose_name='Frecuencia boost (GHz)'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='hilos',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Número de hilos'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='memoria_video',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Memoria VRAM (GB)'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='nucleos',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Número de núcleos'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio_producto',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Precio del producto'),
        ),
    ]
