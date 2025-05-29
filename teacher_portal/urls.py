from django.contrib import admin
from django.urls import path
from portal import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('manage-student/', views.manage_student, name='manage_student'),
    path('student/<int:student_id>/', views.student_detail_view, name='student_detail'),
]