from django.urls import path, include
from rest_framework import routers
from drives.views import DriveViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r'drives', DriveViewSet, 'drives')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/token/obtain/', TokenObtainPairView.as_view()),
    path('api/auth/token/refresh/', TokenRefreshView.as_view()),
]
