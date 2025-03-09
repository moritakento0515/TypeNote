from django.urls import path
from . import views
from django.views.generic.base import RedirectView

app_name = 'tracker'

urlpatterns = [
    path('', RedirectView.as_view(url='scores/', permanent=False)),
    path('scores/', views.user_scores, name='user_scores'),
    path('scores/new_score', views.new_score, name='new_score'),
    path('scores/new_score_create', views.new_score_create, name='new_score_create'),
    path('scores/new_target_score/', views.new_target_score, name='new_target_score'),
    path('scores/new_target_score_create', views.new_target_score_create, name='new_target_score_create'),
    path('scores/history/', views.score_history, name='score_history'),
    path('scores/ranking/', views.community_score_ranking, name='community_score_ranking'),
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('user/<int:user_id>/', views.other_profile_view, name='other_profile_view'),
    
]