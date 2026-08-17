"""
URL configuration for StyleSenseAI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from stylesenseapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.userLogin, name='login'),
    path('logout/<userid>', views.Logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('skinanalysis/', views.skinanalysis, name='skinanalysis'),
    path('virtualtryon/', views.virtualtryon, name='virtualtryon'),
    path('aistylist/', views.aistylist, name='aistylist'),
    path('wardrobe/', views.wardrobe, name='wardrobe'),
    path('history/', views.history, name='history'),
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    # Main skin analysis page (shows latest analysis or upload state)
    path('skin-analysis/', views.skin_analysis_view, name='skin_analysis'),
    
    # Specific skin analysis result page
    path('skin-analysis/<int:analysis_id>/', views.skin_analysis_view, name='skin_analysis_detail'),
]
