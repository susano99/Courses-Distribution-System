from rest_framework import routers
from management.views import CoursesViewSet, RegistrationViewSet


management_router = routers.DefaultRouter()
management_router.register('courses', CoursesViewSet, basename='courses')
management_router.register(
    'registrations', RegistrationViewSet, basename='registrations')
