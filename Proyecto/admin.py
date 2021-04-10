from django.contrib import admin
from advanced_filters.admin import AdminAdvancedFiltersMixin
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from adminfilters.multiselect import UnionFieldListFilter

from .models import Proyecto, Tarea

from django.utils.translation import ugettext_lazy as _


class TareaInline(admin.TabularInline):
	model = Tarea
	extra =0



class ProyectoAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):

	list_display = ["numero", "titulo", "usuario", "socio", "creado_tiempo", "estado"]
	list_display_links = ["numero", "titulo"]
	inlines = [TareaInline]
	search_fields = ["id", 
					"titulo", 
					"usuario__username", 
					"usuario__first_name",
					"socio__nombre",
					"socio__email"
					]

	list_filter = (

		('usuario', RelatedDropdownFilter),
		('estado', UnionFieldListFilter),


	)

	advanced_filters_fields = (
		'usuario__username',
		'socio__nombre',
		'estado',
		'creado_por',
		'titulo',
		'descripcion'

	)

	ordering = ('-creado_por', )
	readonly_fields = ('creado_tiempo', 'ultima_modificacion', 'usuario')
	autocomplete_fields = ["socio"]

	fieldsets = ( #Formularios de edicion

		(None, {'fields': ('titulo', ('usuario', 'socio'), ('estado', ), ('descripcion'))}),

		(_('Mas Campos...'), {'fields': (('creado_tiempo', 'ultima_modificacion'), 'creado_por'), 'classes': ('collapse')})

	)


	def get_fieldsets(self, request, obj=None):
		fieldsets = super().get_fieldsets(request, obj)
		if obj is None:
			fieldsets = (
				(None, {'fields': ('titulo', ('usuario', 'socio'), ('estado', ), ('descripcion'))}),

			)
		return fieldsets

admin.site.register(Proyecto, ProyectoAdmin)
