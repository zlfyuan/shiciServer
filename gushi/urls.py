from django.urls import path

from .views import GushiView, TangShiView, SearchView

urlpatterns = [
    path('savegushi/', GushiView.as_view()),
    path('api/tangshi/', TangShiView.as_view({
        'get': 'list',
    })),
    path('api/tangshi/<int:pk>/', TangShiView.as_view({'get': 'retrieve'})),
    path('api/gushi/', SearchView.as_view()),
]
