from django.urls import path
from . import views
from django.views.generic.base import RedirectView

app_name = 'tracker'

urlpatterns = [
    path('', RedirectView.as_view(url='scores/', permanent=False)),
    path('scores/', views.user_scores, name='user_scores'),
    path('scores/new', views.new, name='new'),
    path('scores/create', views.create, name='create'),
    
    
]