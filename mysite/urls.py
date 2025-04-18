"""
URL configuration for mysite project.

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
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import (
    CustomLoginView,
    RegisterView,
    PictureListView,
    PictureDetailView,
    PictureCreateView,
    PictureUpdateView,
    PictureDeleteView
)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin/', admin.site.urls),

    # Registration URL
    path('register/', RegisterView.as_view(), name='register'),

    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset/password_reset_form.html',
        email_template_name='password_reset/password_reset_email.html',
        subject_template_name='password_reset/password_reset_subject.txt',
        success_url='/password_reset/done/'
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset/password_reset_confirm.html',
        success_url='/reset/done/'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset/password_reset_complete.html'
    ), name='password_reset_complete'),

    # HQ Dog URLs
    path('hq_dogs/', views.hq_dog_list, name='hq_dog_list'),
    path('hq_dogs/<int:pk>/', views.hq_dog_detail, name='hq_dog_detail'),
    path('hq_dogs/create/', views.hq_dog_create, name='hq_dog_create'),
    path('hq_dogs/<int:pk>/update/', views.hq_dog_update, name='hq_dog_update'),
    path('hq_dogs/<int:pk>/delete/', views.hq_dog_delete, name='hq_dog_delete'),
    path('hq_dogs/search/', views.hq_dog_search, name='hq_dog_search'),

    # TPS Moshi Dog URLs
    path('tps_moshi_dogs/', views.tps_moshi_dog_list, name='tps_moshi_dog_list'),
    path('tps_moshi_dogs/<int:pk>/', views.tps_moshi_dog_detail, name='tps_moshi_dog_detail'),
    path('tps_moshi_dogs/create/', views.tps_moshi_dog_create, name='tps_moshi_dog_create'),
    path('tps_moshi_dogs/<int:pk>/update/', views.tps_moshi_dog_update, name='tps_moshi_dog_update'),
    path('tps_moshi_dogs/<int:pk>/delete/', views.tps_moshi_dog_delete, name='tps_moshi_dog_delete'),
    path('tps_moshi_dogs/search/', views.tps_moshi_dog_search, name='tps_moshi_dog_search'),

    # Dodoma Dog URLs
    path('dodoma_dogs/', views.dodoma_dog_list, name='dodoma_dog_list'),
    path('dodoma_dogs/<int:pk>/', views.dodoma_dog_detail, name='dodoma_dog_detail'),
    path('dodoma_dogs/create/', views.dodoma_dog_create, name='dodoma_dog_create'),
    path('dodoma_dogs/<int:pk>/update/', views.dodoma_dog_update, name='dodoma_dog_update'),
    path('dodoma_dogs/<int:pk>/delete/', views.dodoma_dog_delete, name='dodoma_dog_delete'),
    path('dodoma_dogs/search/', views.dodoma_dog_search, name='dodoma_dog_search'),

    # Iringa Dog URLs
    path('iringa_dogs/', views.iringa_dog_list, name='iringa_dog_list'),
    path('iringa_dogs/<int:pk>/', views.iringa_dog_detail, name='iringa_dog_detail'),
    path('iringa_dogs/create/', views.iringa_dog_create, name='iringa_dog_create'),
    path('iringa_dogs/<int:pk>/update/', views.iringa_dog_update, name='iringa_dog_update'),
    path('iringa_dogs/<int:pk>/delete/', views.iringa_dog_delete, name='iringa_dog_delete'),
    path('iringa_dogs/search/', views.iringa_dog_search, name='iringa_dog_search'),

    # HQ Horse URLs
    path('hq_horses/', views.hq_horse_list, name='hq_horse_list'),
    path('hq_horses/<int:pk>/', views.hq_horse_detail, name='hq_horse_detail'),
    path('hq_horses/create/', views.hq_horse_create, name='hq_horse_create'),
    path('hq_horses/<int:pk>/update/', views.hq_horse_update, name='hq_horse_update'),
    path('hq_horses/<int:pk>/delete/', views.hq_horse_delete, name='hq_horse_delete'),
    path('hq_horses/search/', views.hq_horse_search, name='hq_horse_search'),

    # Dodoma Horse URLs
    path('dodoma_horses/', views.dodoma_horse_list, name='dodoma_horse_list'),
    path('dodoma_horses/<int:pk>/', views.dodoma_horse_detail, name='dodoma_horse_detail'),
    path('dodoma_horses/create/', views.dodoma_horse_create, name='dodoma_horse_create'),
    path('dodoma_horses/<int:pk>/update/', views.dodoma_horse_update, name='dodoma_horse_update'),
    path('dodoma_horses/<int:pk>/delete/', views.dodoma_horse_delete, name='dodoma_horse_delete'),
    path('dodoma_horses/search/', views.dodoma_horse_search, name='dodoma_horse_search'),

    # Iringa Horse URLs
    path('iringa_horses/', views.iringa_horse_list, name='iringa_horse_list'),
    path('iringa_horses/<int:pk>/', views.iringa_horse_detail, name='iringa_horse_detail'),
    path('iringa_horses/create/', views.iringa_horse_create, name='iringa_horse_create'),
    path('iringa_horses/<int:pk>/update/', views.iringa_horse_update, name='iringa_horse_update'),
    path('iringa_horses/<int:pk>/delete/', views.iringa_horse_delete, name='iringa_horse_delete'),
    path('iringa_horses/search/', views.iringa_horse_search, name='iringa_horse_search'),

    # Tps Moshi Horse URLs
    path('tps_moshi_horses/', views.tps_moshi_horse_list, name='tps_moshi_horse_list'),
    path('tps_moshi_horses/<int:pk>/', views.tps_moshi_horse_detail, name='tps_moshi_horse_detail'),
    path('tps_moshi_horses/create/', views.tps_moshi_horse_create, name='tps_moshi_horse_create'),
    path('tps_moshi_horses/<int:pk>/update/', views.tps_moshi_horse_update, name='tps_moshi_horse_update'),
    path('tps_moshi_horses/<int:pk>/delete/', views.tps_moshi_horse_delete, name='tps_moshi_horse_delete'),
    path('tps_moshi_horses/search/', views.tps_moshi_horse_search, name='tps_moshi_horse_search'),

    # User URLs
    path('users/', views.user_list, name='user_list'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/update/', views.user_update, name='user_update'),
    path('user/profile/', views.user_profile, name='user_profile'),

    # Medical Record URLs
    path('medical_records/', views.medical_record_list, name='medical_record_list'),
    path('medical_records/<int:pk>/', views.medical_record_detail, name='medical_record_detail'),
    path('medical_records/create/', views.medical_record_create, name='medical_record_create'),
    path('medical_records/<int:pk>/update/', views.medical_record_update, name='medical_record_update'),
    path('medical_records/<int:pk>/delete/', views.medical_record_delete, name='medical_record_delete'),

    # Picture URLs - Using Class-Based Views
    path('pictures/', PictureListView.as_view(), name='picture_list'),
    path('pictures/<int:pk>/', PictureDetailView.as_view(), name='picture_detail'),
    path('pictures/create/', PictureCreateView.as_view(), name='picture_create'),
    path('pictures/<int:pk>/update/', PictureUpdateView.as_view(), name='picture_update'),
    path('pictures/<int:pk>/delete/', PictureDeleteView.as_view(), name='picture_delete'),

    path('activity_logs/', views.activity_log_list, name='activity_log_list'),

    path("logout/", LogoutView.as_view(next_page='login'), name="logout"),

    path('transfers/initiate/', views.transfer_animal_selection, name='initiate_transfer'),
    path('reports/generate/', views.generate_report, name='generate_report'),
    path('animals/add/', views.add_animal_selection, name='add_animal'),

# Add these to your urlpatterns
    path('transfers/', views.transfer_list, name='transfer_list'),
    path('transfers/<int:pk>/', views.transfer_detail, name='transfer_detail'),
    path('transfers/create/', views.transfer_create, name='transfer_create'),
    path('transfers/<int:pk>/update/', views.transfer_update, name='transfer_update'),
    path('transfers/<int:pk>/delete/', views.transfer_delete, name='transfer_delete'),
    path('transfers/<int:pk>/approve/', views.transfer_approve, name='transfer_approve'),
    path('transfers/<int:pk>/report/', views.transfer_report, name='transfer_report'),
]

# Add Django's static file serving configuration during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)