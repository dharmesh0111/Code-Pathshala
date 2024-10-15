"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
path('',views.index ,name='index'),
path('register',views.register),
path('login',views.login_page,name='login_page'),
path('logout',views.logout_page),

    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='resetPassword.html'), 
         name='password_reset'),
    path('password_reset_done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='resetpassword_done.html'), 
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='resetpassword_confirm.html'), 
         name='password_reset_confirm'),
    path('password_reset_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='resetpassword_complate.html'), 
         name='password_reset_complete'),

path('e-learning',views.Elearning),
path('watchonline/<id>',views.watchonline),
path('feedAndRating/<id>',views.feedbackRating),
path('courses/<code>',views.courses),
path("payment/<code>",views.payment),
path("enrolled/<title>",views.enrolled_user),
path('courseMenu',views.course_menu),
path('e-premium',views.premium),
path('watchpremium/<title>',views.watchpremium),
path('coursefeedAndRating/<title>',views.coursefeedbackandrating),
path("support/<title>",views.support),
path('sort/<ord>',views.sortrange),
# path('search-courses',views.searchttitle),
path('search-courses/', views.search_courses, name='search_courses'),

path('chptrlist/<title>',views.chptrlist),
path('chptrlist/watchp/<title>',views.watchchptr),

path('paidcoursereview/<chptr_name>',views.paidcoursereviews),
path('deskboard',views.deskboard),
path('exam/<course_name>',views.giveExam),
# path('info',views.info),
path('mybatch',views.mybatch),
path('question',views.question),
path("progresscard",views.progresscard),
path('message',views.certificate_msg),
path('invoice/<title>',views.generate_invoice),
path('track/<course_name>',views.tracking),


]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

