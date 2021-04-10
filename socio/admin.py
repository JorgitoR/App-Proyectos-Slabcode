from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Socio


class SocioAdmin(admin.ModelAdmin):
	list_display = ["id", "nombre", "email", "website", "telefono", "direcion"]
	list_display_links = ["id", "nombre"]
	search_fields = ["id", "nombre", "email"]

	ordering =["nombre",]
	readonly_fields = ["creado", "ultima_modificacion", "creado_por"]

	fieldsets = ( #Edicion de formularios
		(None, {'fields': (('nombre',), ('email', 'website'), ('telefono', 'direcion'))}),
		(_('Mas campos....'), {'fields': (('creado', 'ultima_modificacion'), 'creado_por'), 'classes': ('collapse',)})
	)


	def get_fieldsets(self, request, obj=None):
		fieldsets = super().get_fieldsets(request, obj)
		if obj is None:
			fieldsets = (
				(None, {'fields': (('nombre',), ('email', 'website'), ('telefono', 'direcion'))}),
			)
		return fieldsets

admin.site.register(Socio, SocioAdmin)