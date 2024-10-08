# Generated by Django 5.1.1 on 2024-10-06 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_tipoproducto_producto'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='capacidad_almacenamiento',
            field=models.IntegerField(blank=True, null=True, verbose_name='Capacidad de almacenamiento (GB)'),
        ),
        migrations.AddField(
            model_name='producto',
            name='frecuencia_base',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Frecuencia base (GHz)'),
        ),
        migrations.AddField(
            model_name='producto',
            name='frecuencia_boost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Frecuencia boost (GHz)'),
        ),
        migrations.AddField(
            model_name='producto',
            name='frecuencia_ram',
            field=models.IntegerField(blank=True, null=True, verbose_name='Frecuencia RAM (MHz)'),
        ),
        migrations.AddField(
            model_name='producto',
            name='hilos',
            field=models.IntegerField(blank=True, null=True, verbose_name='Número de hilos'),
        ),
        migrations.AddField(
            model_name='producto',
            name='marca',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Marca del producto'),
        ),
        migrations.AddField(
            model_name='producto',
            name='memoria_video',
            field=models.IntegerField(blank=True, null=True, verbose_name='Memoria VRAM (GB)'),
        ),
        migrations.AddField(
            model_name='producto',
            name='modelo',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Modelo del producto'),
        ),
        migrations.AddField(
            model_name='producto',
            name='nucleos',
            field=models.IntegerField(blank=True, null=True, verbose_name='Número de núcleos'),
        ),
        migrations.AddField(
            model_name='producto',
            name='tipo_memoria',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Tipo de memoria'),
        ),
        migrations.AddField(
            model_name='producto',
            name='velocidad_escritura',
            field=models.IntegerField(blank=True, null=True, verbose_name='Velocidad de escritura (MB/s)'),
        ),
        migrations.AddField(
            model_name='producto',
            name='velocidad_lectura',
            field=models.IntegerField(blank=True, null=True, verbose_name='Velocidad de lectura (MB/s)'),
        ),
    ]
