from django.urls import path


from .views import (inicio, Login, 
					Logout, CrearUsuarioView,
					CrearProyectoAPIView, ProyectoListaAPIView,
					TareaListaAPIView, 
					RegistrarView, CrearTareaAPIView)

from rest_framework.authtoken import views

urlpatterns = [

	path('proyectos/', ProyectoListaAPIView.as_view(), name='ProyectoListaAPIView'), #api/proyectos/
	path('crear/', CrearUsuarioView.as_view(), name='CrearUsuarioView'),
	
	path('crear_proyecto/', CrearProyectoAPIView.as_view(), name='CrearProyectoAPIView'),
	path('crear_tarea/proyecto/<int:proyecto_id>/', CrearTareaAPIView.as_view(), name='CrearTareaAPIView'),
	

	path('tareas/', TareaListaAPIView.as_view(), name='TareaListaAPIView'),
	
	path('registro_usuario/', RegistrarView.as_view(), name='RegistrarView'),
	
    path('api_generate_token/', views.obtain_auth_token),

	path('login/', Login.as_view(), name='login'),
	path('logout/', Logout.as_view(), name='logout'),


]