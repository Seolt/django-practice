from django.urls import path, include, re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
app_name='Wendy'
urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    # path('sign-in/', views.login, name='login'),
    path('sign-in/',views.login, name='login'),
    path('register/', views.register, name='register'),
    path('change-password/',views.changepassword, name='changepassword'),
    path('logout/',views.logout, name='logout'),
    path('email_send/',views.send_Email, name='send_email'),
    path('my-profile/', views.upload_profile, name='upload_profile'),
    path('bookmarks/',views.bookmark, name='bookmark'),
    path('my-ads/',views.my_ads, name='my_ads'),
    path('sold-items/',views.sold_items, name='sold_items'),
    path('manage-permissions/', views.manage_permissions, name='manage_permissions'),
    path('<str:url>/', views.dynamic_url, name='url'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)