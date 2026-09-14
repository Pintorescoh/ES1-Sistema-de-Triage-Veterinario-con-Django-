from django.contrib import admin
from django.urls import path
from recepcion import views # Importamos las vistas de tu aplicación

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rutas para el CRUD de los pacientes
    path('pacientes/', views.lista, name='lista'),
    path('pacientes/crear/', views.crear, name='crear'),
    path('pacientes/<int:pk>/editar/', views.editar, name='editar'),
    path('pacientes/<int:pk>/eliminar/', views.eliminar, name='eliminar'),
    
    # Rutas de seguridad
    path('login/', views.vista_login, name='login'),
    path('logout/', views.vista_logout, name='logout'),
]