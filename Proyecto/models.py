from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from Prueba.db.models import EstadoDelProyecto
from django.urls import reverse

from socio.models import Socio
from django.conf import settings

from Prueba.db.mail import send_mail_async as send_mail

import logging
from hashlib import sha1

logger = logging.getLogger(__name__)

User = settings.AUTH_USER_MODEL


			
class Proyecto(models.Model):

	ESTADOS = (
		('para_hacer', ('PARA HACER')),
		('en_proceso', ('En Proceso')),
		('bolqueado', ('Bloqueado')),
		('Hecho', ('Hecho')),
		('descartado', ('Descartado'))

	)
	titulo = models.CharField(max_length=200)
	socio = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
	descripcion = models.TextField()

	usuario = models.ForeignKey(User, related_name='tareas_asignada', 
		verbose_name="asignado a", on_delete=models.SET_NULL, null=True)	

	estado = models.CharField(verbose_name="Estado", max_length=20, choices=ESTADOS, default='para_hacer')

	creado_por = models.ForeignKey(User, related_name='usuario_creado', 
		verbose_name='Creado Por', on_delete=models.SET_NULL, null=True)

	creado_tiempo = models.DateTimeField(verbose_name='creado', auto_now_add=True, editable=False)
	ultima_modificacion = models.DateTimeField(verbose_name='Ultima Modificacion', auto_now=True, editable=False)

	def __str__(self):
		return self.titulo

	def __str__(self):
		return "[%s] %s" % (self.numero, self.titulo)	

	@property
	def numero(self):
		return '{:08d}'.format(self.pk)


	def get_absolute_url(self):
		return reverse("detail", kwargs={"pk":self.pk})

	def save(self, *args, **kwargs):
		tarea_creada = self.pk is None
		super().save(*args, **kwargs)
		if tarea_creada:
			self.send_nueva_tarea_email()

	def send_nueva_tarea_email(self):

		"""
		Anular con un correo electrónico personalizado
		"""
		emails = []
		print(emails)
		if self.socio.email:
			print(self.socio.email)
			emails.append(self.socio.email)
		if settings.TASKS_SEND_EMAILS_TO_ASSIGNED and getattr(self, "usuario", None) and self.usuario.email:
			emails.append(self.usuario.email)
		if len(emails):
			logger.info("[Tarea #%s] Enviando tareas creadas al correo: %s", self.numero, emails)
			values = {

				"id": self.numero,
				"usuario": str(self.usuario) if getattr(self, "usuario", None) else '(No hay asignado aun)',
				"titulo": self.titulo,
				"descripcion": self.descripcion or '-',
				"sign": settings.SITIO_HEADER,

			}

			if settings.TASKS_VIEWER_ENABLED:
				email_template = settings.MTASKS_EMAIL_WITH_URL
				values["url"] = self.get_tarea_url_viewer()
			else:
				email_template = settings.MTASKS_EMAIL_WITHOUT_URL

			try:
				send_mail(

					'[{aplicacion}] [#{id}] Nueva Tarea Creada'.format(aplicacion=settings.APP_NAME, id=self.numero),
					email_template.format(**values),
					settings.APP_EMAIL,
					emails,

				)
			except Exception as e:
				logger.warning("[Tarea #%S] Error tratando de enviar un Email a la tarea creada - %s: %s",
							self.numero, e.__class__.__name__, str(e)
						)

	def get_tarea_url_viewer(self):


		salt = settings.TASKS_VIEWER_HASH_SALT
		if not settings.DEBUG and salt == '1two3':
			logger.warning("Codigo de sal inseguro utilizado para enviar pedidos por correo electronico, NO lo use en PRODUCCION")

			token = "{}-{}".format(salt, self.pk)
			token = sha1(token.encode('utf-8')).hexdigest()
			return settings.TASKS_VIEWER_ENDPOINT.format(number=self.numero, token=token)



class Tarea(models.Model):

	proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	descripcion = models.CharField(verbose_name="Titulo", max_length=200)	
	terminado = models.BooleanField(verbose_name="¿Terminado?", default=False)

	fecha = models.DateField(verbose_name='Fecha de Ejecucion')

	def __str__(self):
		return self.descripcion

