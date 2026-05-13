from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns=[
             path('signup/', views.signup, name='signup'),
             path('login/', views.loginPage, name='login'),
             path('logout/',views.logoutUser, name='logout'),
             path("predict/", views.predict_view, name="predict"),
             path("profile/edit/", views.edit_profile, name="edit_profile"),
             path("history/", views.prediction_history, name="history"),
             path("generate-report/", views.generate_report, name="generate_report"),
            ]



urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)



