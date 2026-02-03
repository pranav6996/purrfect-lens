from django.contrib import admin
from django.urls import path, include
from cats import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('breeds/', views.breed_list, name='breed_list'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/predict/', views.predict_breed, name='predict_api'),
    path('api/fact/', views.get_random_fact, name='fact_api'),
]
