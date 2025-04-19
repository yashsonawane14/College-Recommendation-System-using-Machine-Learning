from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Recommendation and comparison features
    path('recommendation/', views.recommendation, name='recommendation'),
    path('compare/', views.compare, name='compare'),
    path('search/', views.search_college, name='search_college'),
    path('recommendation_form/', views.recommendation_view, name='recommendation_form'),
    path('discard/', views.discard_college, name='discard_college'),
    path("get_college_names/", views.get_college_names, name="get_college_names"),
    # Additional services page from code1
    path('services/', views.services, name='services'),

    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('activate/<email_token>',views.activate_email, name="activate_email"),

    # Chatbot API
    path('chatbot/', views.chatbot_view, name='chatbot_api'),
]
