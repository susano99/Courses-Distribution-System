from django_filters import CharFilter, FilterSet, NumberFilter, OrderingFilter
from .models import Course, Registration

class CourseFilter(FilterSet, OrderingFilter):
    
    code = CharFilter(field_name="code", lookup_expr="icontains")
    language = CharFilter(field_name="language", lookup_expr="icontains")
    major = CharFilter(field_name="major", lookup_expr="icontains")

    class Meta:
        model = Course
        fields = [
            "code",
            "language",
            "major"
        ]
        

class RegistrationFilter(FilterSet, OrderingFilter):
    
    year = CharFilter(field_name="year", lookup_expr="icontains")

    class Meta:
        model = Registration
        fields = [
            "year",
        ]