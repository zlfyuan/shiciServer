from django.urls import path

from .views import GushiView, SearchView, SaveView, PinyinView, StrainsView

urlpatterns = [
    path('savegushi/', SaveView.as_view()),
    path('api/gushi/<str:type>/', GushiView.as_view({'get': 'list'})),
    path('api/gushi/<str:type>/<int:pk>/', GushiView.as_view({'get': 'retrieve'})),
    path('api/gushi/update/<str:type>/<int:pk>/', GushiView.as_view({'post': 'update'})),

    path('api/shici/pinyin/<int:pk>/', PinyinView.as_view({'get': 'retrieve'})),
    path('api/shici/pinyin/update/<int:pk>/', PinyinView.as_view({'post': 'update'})),

    path('api/shici/strains/<int:pk>/', StrainsView.as_view({'get': 'retrieve'})),
    path('api/shici/strains/update/<int:pk>/', StrainsView.as_view({'post': 'update'})),


    path('api/shici/search/', SearchView.as_view())
]
