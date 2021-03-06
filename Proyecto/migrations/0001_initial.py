# Generated by Django 3.2 on 2021-04-09 22:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('estado', models.CharField(choices=[('para_hacer', 'PARA HACER'), ('en_proceso', 'En Proceso'), ('bolqueado', 'Bloqueado'), ('Hecho', 'Hecho'), ('descartado', 'Descartado')], default='para_hacer', max_length=20, verbose_name='Estado')),
                ('creado_tiempo', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('ultima_modificacion', models.DateTimeField(auto_now=True, verbose_name='Ultima Modificacion')),
                ('creado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usuario_creado', to=settings.AUTH_USER_MODEL, verbose_name='Creado Por')),
                ('socio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='socio.socio')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tareas_asignada', to=settings.AUTH_USER_MODEL, verbose_name='asignado a')),
            ],
        ),
        migrations.CreateModel(
            name='TareaUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=200, verbose_name='Descripcion')),
                ('terminado', models.BooleanField(default=False, verbose_name='??Terminado?')),
                ('fecha', models.DateField()),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Proyecto.proyecto')),
                ('usuario_tarea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Proyecto.tareausuario')),
            ],
        ),
    ]
