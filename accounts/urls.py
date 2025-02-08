from django.urls import path
from . import views
from django.views.generic.base import RedirectView

app_name = 'accounts'

urlpatterns = [
    path('', RedirectView.as_view(url='signup/', permanent=False)),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    
    
]
