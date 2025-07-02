from django.urls import path
from . import views
app_name = 'quotes'
urlpatterns = [
    path('', views.random_quote, name='random'),
    path('add/', views.add_quote, name='add'),
    path('quote/<int:pk>/vote/', views.vote_quote, name='vote'),
    path('top/', views.top_quotes, name='top'),
]