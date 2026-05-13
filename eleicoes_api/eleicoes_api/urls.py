from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from urna import views

#configurando o swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="API de Eleições",
      default_version='v1',
      description="API para gerenciamento de eleições, candidatos e votos",
      contact=openapi.Contact(email="contato@eleicoes.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'eleitores', views.EleitorViewSet, basename='eleitores')
router.register(r'eleicoes', views.EleicaoViewSet, basename='eleicoes')
router.register(r'candidatos', views.CandidatoViewSet, basename='candidatos')
router.register(r'aptidoes', views.AptidaoEleitorViewSet, basename='aptidoes')
router.register(r'registro-votacao', views.RegistroVotacaoViewSet, basename='registro-votacao')
router.register(r'votos', views.VotoViewSet, basename='votos')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]