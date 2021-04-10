from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Socio(models.Model):
	"""
	Socio o partner es el Operador 
	"""

	nombre = models.CharField(verbose_name="Nombre", max_length=200)
	email  = models.EmailField(verbose_name="Email")
	website = models.URLField(verbose_name="WebSite", blank=True)

	telefono = models.CharField(verbose_name="Telefono", max_length=10, null=True, blank=True)
	direcion = models.CharField(verbose_name="Direccion", max_length=40, null=True, blank=True)

	creado_por = models.ForeignKey(User, related_name='tareas_creadas', 
		verbose_name="Creado Por", on_delete=models.SET_NULL, null=True)

	creado = models.DateTimeField(auto_now_add=True, editable=False)
	ultima_modificacion = models.DateTimeField(auto_now=True, editable=False)

	def __str__(self):
		return self.nombre

	class Meta:
		ordering = ["nombre"]
		verbose_name = "Socio"
		verbose_name_plural = "Socios"