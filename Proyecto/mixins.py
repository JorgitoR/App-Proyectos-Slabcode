from django import forms
from django.forms.utils import ErrorList

class FormularioMixin(object):
	def form_valid(self, form):
		if self.request.user.is_authenticated:
			form.instance.usuario = self.request.user
			return super(FormularioMixin, self).form_valid(form)
		else:
			form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["Usuario No logueado"])
			return self.form_invalid(form)