from django.contrib import admin
from django.urls import path, include
from core import urls as api_urls
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('api-auth/', include('rest_framework.urls')),
    # path('auth-token/', views.CustomObtainAuthTokenView.as_view()),
    path('', include(api_urls)),
]
