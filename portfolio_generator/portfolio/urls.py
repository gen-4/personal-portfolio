from django.urls import path
from portfolio import views

portfolio_urls = [
    path('', views.get_main_page, name='main-page'),
    path('project/<project_name>', views.get_project, name='project-page')
]