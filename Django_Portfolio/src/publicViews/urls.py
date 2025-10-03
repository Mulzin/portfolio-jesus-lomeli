from django.urls import path

from . import views

urlpatterns = [
    path("", views.english_home, name='root'),
    path('sp_home', views.spanish_home),
    path('en_home', views.english_home),
    path("api/get_portfolio",views.get_portfolio,name='portfolio-data')
]