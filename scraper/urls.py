from django.urls import path
from . import views

app_name = 'scraper'

urlpatterns = [
    path('', views.index, name='index'),
    path('scrape/', views.scrape_view, name='scrape'),
    path('history/', views.get_history, name='history'),
]
