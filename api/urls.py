from rest_framework import routers
from django.urls import path

from . import views


urlpatterns = [
    path('', views.apiOverview, name="api-overview"),
	path('cuboid-list-all/', views.cuboidALListView.as_view(), name="cuboid-list"),
	path('cuboid-list/', views.cuboidListView.as_view(), name="cuboid-list"),
	path('cuboid-create/', views.cuboidCreate, name="cuboid-create"),
	path('cuboid-update/<str:pk>/', views.cuboidUpdate, name="cuboid-update"),
	path('cuboid-delete/<str:pk>/', views.cuboidDelete, name="cuboid-delete"),
]


