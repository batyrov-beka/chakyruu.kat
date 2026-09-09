from django.urls import path
from . import views

urlpatterns = [
path('', views.home_view, name='home'),
    path('<slug:slug>/', views.invitation_detail, name='invitation_detail'),
]