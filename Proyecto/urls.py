from django.urls import path

from .views import  (ProyectoCrear, proyecto_detail, 
				CrearTask, Toogle, eliminar_tarea, editar_tarea, MisTareas)

urlpatterns = [
	

    path('crear/', ProyectoCrear.as_view(), name='crearProyect'),
    path('proyecto_detail<int:pk>/', proyecto_detail, name='detail'),
    path('proyecto/<int:pk>/crear_tarea/', CrearTask, name='CrearTarea'),
    path('toogle/<proyecto_id>', Toogle, name='toogle'),
    path('mis_tareas/', MisTareas, name='mis_tareas'),


    path('editar_tarea/<tarea_id>', editar_tarea, name='edit'),
    path('eliminar_tarea/<tarea_id>', eliminar_tarea, name='delete'),

    


]