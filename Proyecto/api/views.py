from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.response import Response


from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView

from django.contrib.auth import login, logout, authenticate 
from django.contrib.auth.forms import AuthenticationForm

from django.http import HttpResponseRedirect

from Proyecto.models import  Proyecto, Tarea
from .serializers import ( 
						  UsuarioSerializer, 
						  TareaSerializer,
						  ProyectoSerializer,
						  RegistrarSerializer)

from django.contrib.auth import get_user_model

from .pagination import ResultadoStandarPaginacion

Usuario = get_user_model()

class inicio(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		context ={'mensage':'Hola Mundo'}
		return Response(context)


class CrearUsuarioView(generics.CreateAPIView):
	"""
	Crear el usuario
	"""
	model = get_user_model()
	permission_classes = [permissions.AllowAny]
	serializer_class = UsuarioSerializer



class RegistrarView(generics.CreateAPIView):
	"""
	Hola desde unidad
	"""
	queryset = Usuario.objects.all()
	permission_classes=[permissions.AllowAny]
	serializer_class = RegistrarSerializer


class CrearProyectoAPIView(generics.CreateAPIView):

	"""
	Creamos el Proyecto.
	 Campos:
	 		Usuario quien lo crea 
	 		titulo
	        Descripcion
	        Socio, un operador quien puede añadir, eliminar y editar las tareas
	        Fecha de creacion

	"""
	serializer_class = ProyectoSerializer
	permission_classes = [permissions.IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(creado_por=self.request.user)


class CrearTareaAPIView(generics.CreateAPIView):
	serializer_class = TareaSerializer
	permission_classes = [permissions.IsAuthenticated]

	def perform_create(self, serializer):

		proyecto_id = self.kwargs.get('proyecto_id')
		proyecto  = get_object_or_404(Proyecto, pk=proyecto_id)

		if self.request.user == proyecto.creado_por or self.request.user== proyecto.socio or self.request.user.is_staff: 
			serializer.save(proyecto=proyecto, usuario=self.request.user)
		
	
class ProyectoListaAPIView(generics.ListAPIView):

	"""
	Retornamos un Queryset de todo los proyectos creados

	"""

	serializer_class = ProyectoSerializer
	pagination_class = ResultadoStandarPaginacion
	permission_classes = [permissions.AllowAny]

	def get_queryset(self, *args, **kwargs):
		qs =  Proyecto.objects.all().order_by("creado_tiempo")
		query = self.request.GET.get("q", None)
		print('QUERRRRR',  query)
		if query is not None:
			qs =qs.filter(
				Q(nombre__icontains=query)|
				Q(usuario__username__icontains=query)
				)
		return qs


class TareaListaAPIView(generics.ListAPIView):
	queryset = Tarea.objects.all()
	serializer_class = TareaSerializer
	pagination_class = ResultadoStandarPaginacion
	permission_classes = [permissions.AllowAny]

class Login(FormView):
	template_name='login.html'
	form_class = AuthenticationForm
	success_url = reverse_lazy('inicio')

	@method_decorator(csrf_protect)
	@method_decorator(never_cache)
	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return HttpResponseRedirect(self.get_success_url())
		else:
			return super(Login, self).dispatch(request, *args, **kwargs)


	def form_valid(self, form):
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		usuario = authenticate(username=username, password=password)
		token, created = Token.objects.get_or_create(user=usuario)
		if token:
			login(self.request, form.get_user())
			return super(Login, self).form_valid(form)

class Logout(APIView):
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		request.user.auth_token.delete()
		logout(request)
		return Response(status=status.HTTP_200_OK)