from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('alfissen-dashboard/', views.AlfissenDashboardView.as_view(), name='alfissen_dashboard'),
    path('ouakkaha-dashboard/', views.OuakkahaDashboardView.as_view(), name='ouakkaha_dashboard'),
] 