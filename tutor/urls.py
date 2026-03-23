from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Primary and Secondary School Pages
    path('primary-school/', views.primary_school, name='primary_school'),
    path('secondary-school/', views.secondary_school, name='secondary_school'),

    # CAPS Content Generator (AJAX GET)
    path('generate-caps-content/', views.generate_caps_content, name='generate_caps_content'),
]
