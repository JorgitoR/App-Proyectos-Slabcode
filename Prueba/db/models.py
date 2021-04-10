from django.db import models

class EstadoDelProyecto(models.TextChoices):
	PUBLICADO = 'PU', 'Publicado'
	BORRADOR  = 'BO', 'Borrador'