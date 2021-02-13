from django.urls import include, path
from rest_framework import routers
from annonces import views

router = routers.DefaultRouter()
router.register(r'annonces', views.AnnonceViewSet)

app_name = "annonces"

urlpatterns = [
    path('', include(router.urls)),
    path('annonces/', include('rest_framework.urls', namespace='rest_framework'))
]