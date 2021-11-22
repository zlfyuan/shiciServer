from django.urls import path

from .views import GushiView, TangShiView, SearchView, TangShiSanBaiView, SongCiView, SongCiSanBaiView

urlpatterns = [
    path('savegushi/', GushiView.as_view()),
    path('api/tangshi/', TangShiView.as_view({'get': 'list'})),
    path('api/tangshi/<int:pk>/', TangShiView.as_view({'get': 'retrieve'})),

    path('api/tangshisanbai/', TangShiSanBaiView.as_view({'get': 'list'})),
    path('api/tangshisanbai/<int:pk>/', TangShiSanBaiView.as_view({'get': 'retrieve'})),

    path('api/songci/', SongCiView.as_view({'get': 'list'})),
    path('api/songci/<int:pk>/', SongCiView.as_view({'get': 'retrieve'})),

    path('api/songcisanbai/', SongCiSanBaiView.as_view({'get': 'list'})),
    path('api/songcisanbai/<int:pk>/', SongCiSanBaiView.as_view({'get': 'retrieve'})),

    path('api/gushi/search/', SearchView.as_view()),
]
