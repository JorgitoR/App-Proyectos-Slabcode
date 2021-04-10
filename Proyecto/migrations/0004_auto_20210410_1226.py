# Generated by Django 3.2 on 2021-04-10 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proyecto', '0003_alter_proyecto_socio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarea',
            name='descripcion',
            field=models.CharField(max_length=200, verbose_name='Titulo'),
        ),
        migrations.AlterField(
            model_name='tarea',
            name='fecha',
            field=models.DateField(verbose_name='Fecha de Ejecucion'),
        ),
    ]
