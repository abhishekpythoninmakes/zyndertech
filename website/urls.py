from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services_list, name='services'),
    path('service/<int:pk>/', views.service_detail, name='service_detail'),
    path('trainings/', views.trainings_list, name='trainings'),
    path('training/<int:pk>/', views.training_detail, name='training_detail'),
    path('contact/', views.contact_view, name='contact'),
    path('contact_new/',views.contact_view_new,name='contact_new'),
    path('api/search/', views.live_search, name='live_search'),
]