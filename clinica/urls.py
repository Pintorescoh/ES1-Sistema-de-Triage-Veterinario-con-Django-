from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from recepcion import views # Importamos las vistas de tu aplicación
from recepcion.api_views import PacienteViewSet, TokenConLimiteView

# El router genera solo las rutas REST del ViewSet (listar, crear, ver, editar, borrar)
router = DefaultRouter()
router.register(r"pacientes", PacienteViewSet, basename="paciente")

urlpatterns = [
    path('admin/', admin.site.urls),

    # API REST (ES3): vive aparte, bajo /api/
    path('api/token/', TokenConLimiteView.as_view(), name='api_token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
    path('api/', include(router.urls)),

    # Rutas para el CRUD de los pacientes
    path('pacientes/', views.lista, name='lista'),
    path('pacientes/crear/', views.crear, name='crear'),
    path('pacientes/<int:pk>/editar/', views.editar, name='editar'),
    path('pacientes/<int:pk>/eliminar/', views.eliminar, name='eliminar'),

    # Rutas de seguridad
    path('login/', views.vista_login, name='login'),
    path('logout/', views.vista_logout, name='logout'),
]

# Documentación de la API (Swagger): solo en desarrollo. Muestra la estructura,
# no los datos; para probar endpoints desde ahí igual se necesita el token JWT.
if settings.DEBUG:
    urlpatterns += [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='api_docs'),
    ]
