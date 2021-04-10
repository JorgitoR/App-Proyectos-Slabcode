from django import forms
from .models import Proyecto, Tarea
from datetime import datetime, timedelta
from django.forms.fields import DateField

class ProyectoForm(forms.ModelForm):

	class Meta:
		model = Proyecto
		fields = [

			"titulo",
			"socio",
			"descripcion",
			"usuario",
			"estado",

		]

		widgets = {

			'titulo':forms.TextInput(
				attrs = {'class':'form-control', 'placeholder':'Escribe el Titulo del proyecto'}

			),
			'socio':forms.Select(
				attrs = {'class':'form-control'}

			),
	
			'descripcion':forms.Textarea (
				attrs = {'class':'form-control', 
						'id':'exampleFormControlTextarea1', 
						'rows':'3', 
						'placeholder':'Escribe la descripcion del Proyecto'}
			),

			'usuario':forms.Select(
				attrs = {'class':'form-control'}

			),

			'estado':forms.Select(
				attrs = {'class':'form-control'}

			),
		}




class TareaForm(forms.ModelForm):

	fecha = DateField(widget=forms.DateInput(attrs={'placeholder': "YYY-MM-DD", 'required':'required'}))	
	terminado = forms.BooleanField(required=False)
	class Meta:
		model = Tarea
		fields =[

			"descripcion",
			"fecha"
		]

	def clean(self):
		limpiar = self.cleaned_data
		datos2 = limpiar.get('fecha')
		if str(datos2)<=(datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'):
			raise forms.ValidationError("La fecha no puede ser del pasado")
		return limpiar