from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.timesince import timesince

from Proyecto.models import  Proyecto, Tarea

from socio.api.serializers import SocioSerializer


from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


from datetime import datetime, timedelta
from django.forms.fields import DateField

import logging
from hashlib import sha1

logger = logging.getLogger(__name__)
Usuario = get_user_model()


from Prueba.db.mail import send_mail_async as send_mail
from django.conf import settings

class UsarioDisplaySerializer(serializers.ModelSerializer):

	class Meta:
		model = Usuario
		fields = [
			'username',
			'first_name',
			'last_name',


		]


class ProyectoSerializer(serializers.ModelSerializer):

	usuario = UsarioDisplaySerializer(read_only=True)
	creado_por = UsarioDisplaySerializer(read_only=True)
	class Meta:
		model = Proyecto
		fields = [
			'id',
			'numero',
			'creado_por',
			'titulo',
			'socio',
			'usuario',
			'descripcion',
			'estado',
			'creado_tiempo'

		]

	def get_fecha_display(self, obj):
		return obj.creado_tiempo.strftime("%b %d %I:%M %p")

	def get_timesince(self, obj):
		return timesince(obj.creado_tiempo) + "Hace"



class RegistrarSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(
			required=True,
			validators = [UniqueValidator(queryset=Usuario.objects.all())]
		)

	password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
	password2 = serializers.CharField(write_only=True, required=True)


	class Meta:
		model = Usuario
		fields = [
			"username",
			"password",
			"password2",
			"email",
			"first_name",
			"last_name"

		]

		extra_kwargs = {
			'first_name':{"required":True},
			'last_name':{"required":True}
		}


	def validate(self, attrs):
		if attrs['password']  != attrs['password2']:
			raise serializers.ValidationError({'password':'Las contraseña no concuerdan'})

		return attrs


	def create(self, validated_data):
		usuario = Usuario.objects.create(

			username = validated_data['username'],
			email = validated_data['email'],
			first_name = validated_data['first_name'],
			last_name = validated_data['last_name']
		)

		usuario.set_password(validated_data['password'])

		usuario.save()

		if usuario:
			self.enviar_email(usuario)

		return usuario


	def enviar_email(self, obj):
		email = []

		if obj.email:
			print(obj.email)
			email.append(obj.email)
		if len(email):
			logger.info("[Usuario %s] Enviando credenciales al correo %s", obj.username, obj.email)
			values = {

				'nombre':obj.first_name,
				'apellido':obj.last_name,
				'titulo':'Credenciales De inicio de sesion',
				'username': obj.username,
				'password': 'clave1234',
				'sign': settings.SITIO_HEADER,

			}

		email_template = settings.CREDENCIALES_USUARIO

		try:
			send_mail(

				'[{app}][{usuario}] Credenciales de inicio de sesion'.format(app=settings.APP_NAME, usuario=obj.username),
				email_template.format(**values),
				settings.APP_EMAIL,
				email

			)
		except Exception as e:
			logger.warning("[Tarea #%S] Error tratando de enviar un Email a la tarea creada - %s: %s",
							obj.username, e.__class__.__name__, str(e)
						)


class UsuarioSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)

	def create(self, validated_data):
		user = Usuario.objects.create(
			username = validated_data['username']
		)
		user.set_password(validated_data['password'])
		user.save()

		return user

	class Meta:
		model = Usuario
		fields = ("id", "username", "password")



class TareaSerializer(serializers.ModelSerializer):

	usuario = UsarioDisplaySerializer(read_only=True)
	proyecto = ProyectoSerializer(read_only=True)

	class Meta:
		model = Tarea
		fields = (

			'proyecto',
			'usuario',
			'descripcion',
			'terminado',
			'fecha'


		)

	def clean(self, obj):
		limpiar = obj.cleaned_data
		datos2 = limpiar.get('fecha')
		if str(obj.fecha)<=(datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'):
			raise serializers.ValidationError("La fecha no puede ser del pasado")
		return obj