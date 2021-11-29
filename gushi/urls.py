from django.urls import path

from .views import GushiView, SearchView

urlpatterns = [
    # path('savegushi/', GushiView.as_view()),
    path('api/gushi/<str:type>/', GushiView.as_view({'get': 'list'})),
    path('api/gushi/<str:type>/<int:pk>/', GushiView.as_view({'get': 'retrieve'})),
    path('api/gushi/update/<str:type>/<int:pk>/', GushiView.as_view({'post': 'update'})),

    path('api/gushi/search/', SearchView.as_view())
]
