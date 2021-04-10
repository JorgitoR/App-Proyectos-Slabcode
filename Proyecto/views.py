from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
				CreateView,
				DetailView,
				DeleteView,
				ListView,
				UpdateView
				)

from .models import Proyecto, Tarea
from .forms import ProyectoForm, TareaForm

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


from django.contrib.auth import authenticate, login, logout

from django.db.models import Q

from .mixins import FormularioMixin
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect

class ProyectoLista(ListView):

	def get_queryset(self, *args, **kwargs):
		qs = Proyecto.objects.all()
		query = self.request.GET.get("q", None)
		if query is not None:
			qs = qs.filter(
				Q(nombre__icontains=query) |
				Q(usuario__username__icontains=query)
			)
		return qs 

	def get_context_data(self, *args, **kwargs):
		context = super(ProyectoLista, self).get_context_data(*args, **kwargs)
		context['crear_proyecto'] = ProyectoForm()
		context['crear_url'] = reverse_lazy("crearProyect")
		context['lista'] = Proyecto.objects.all()
		return context


class ProyectoCrear(FormularioMixin, CreateView):
	form_class = ProyectoForm
	template_name='proyecto/crear.html'


def Toogle(request, proyecto_id):


	project  = get_object_or_404(Proyecto, pk=proyecto_id)
	tarea_obj = Tarea.objects.filter(proyecto=project).order_by('fecha')

	msg = False
	if (request.POST.get('terminado', False) == False):
		msg=True
		context = {
			'tarea_obj':tarea_obj,
			'msg':msg,
			'project':project
		}
		return render(request, 'TareApp/Tarea.html', context)


	if request.method=='POST':
		value = request.POST.get('terminado', None)
		tarea = Tarea.objects.get(id=value)
		tarea.terminado = True
		tarea.save()

		tarea_qs = Tarea.objects.filter(proyecto=project).exclude(terminado=True)
		if not tarea_qs.exists():
			proyecto = Proyecto.objects.get(id=proyecto_id)
			proyecto.estado = 'Hecho'
			proyecto.save()


	context = {
		'tarea_obj':tarea_obj,
		'msg':msg,
		'project':project

	}

	return render(request, 'TareApp/Tarea.html', context)


def eliminar_tarea(request, tarea_id):
	tarea = Tarea.objects.get(pk=tarea_id)
	deleted = False


	if request.user.is_authenticated:
		if request.user == tarea.proyecto.creado_por or request.user==tarea.proyecto.socio or request.user.is_staff:
			tarea.delete()
			deleted=True
			return redirect('toogle', tarea.proyecto.id)
		else:
			raise PermissionDenied
	
	tarea_obj = Tarea.objects.filter(usuario=request.user).order_by("fecha")

	context = {
		'tarea':tarea,
		'tarea_obj':tarea_obj,
		'deleted':deleted
	}

	return render(request, 'TareApp/Tarea.html', context)


def editar_tarea(request, tarea_id):
	tarea_pk = Tarea.objects.get(pk=tarea_id)
	edited = False


	if not request.user.is_authenticated:
		raise PermissionDenied

	if request.user == tarea_pk.proyecto.creado_por or request.user== tarea_pk.proyecto.socio or request.user.is_staff:

		if request.method =='POST':
			form = TareaForm(data=request.POST, instance=tarea_pk)
			if form.is_valid():
				edited =True
				form.save()
				return redirect('toogle', tarea_pk.proyecto.id)	
			else:
				print(form.errors)

		else:
			form = TareaForm()

	else:
		raise PermissionDenied

	context = {
		'tarea_obj':tarea_pk,
		'edited':edited,
		'form':form
	}

	return render(request, 'TareApp/editar.html', context)

def CrearTask(request, pk):

	if not request.user.is_authenticated:
		raise PermissionDenied

	proyecto = get_object_or_404(Proyecto, pk=pk)

	if request.user == proyecto.creado_por or request.user==proyecto.socio or request.user.is_staff:

		if request.method == 'POST':
			form = TareaForm(request.POST)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.proyecto = proyecto
				instance.usuario = request.user
				instance.save()

				proyecto = Proyecto.objects.get(id=pk)
				proyecto.estado = 'en_proceso'
				proyecto.save()

				return redirect("toogle", proyecto.pk)
		else:
			form = TareaForm()


	else:
		raise PermissionDenied

	context = {

		'proyecto':proyecto,
		'form':form

	}

	return render(request, 'proyecto/crear_tarea.html', context)



def MisTareas(request):
	tarea_obj = Tarea.objects.filter(usuario=request.user).order_by('fecha')

	context = {
		'tarea_obj':tarea_obj
	}

	return render(request, 'TareApp/mis_tareas.html', context)

def proyecto_detail(request, pk=None):
	
	instance = get_object_or_404(Proyecto, pk=pk)
	
	context = {
		"instance":instance
	}
	return render(request, 'proyecto/detail.html', context)



