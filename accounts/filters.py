from django.contrib.auth.models import Permission
from django_filters import CharFilter, FilterSet, NumberFilter, OrderingFilter
from .models import Doctor


class DoctorFilter(FilterSet, OrderingFilter):
    
    first_name = CharFilter(field_name="first_name", lookup_expr="icontains")
    father_name = CharFilter(field_name="father_name", lookup_expr="icontains")
    last_name = CharFilter(field_name="last_name", lookup_expr="icontains")
    email = CharFilter(field_name="email", lookup_expr="icontains")
    aca_degree = CharFilter(field_name="aca_degree", lookup_expr="icontains")
    contract_type = CharFilter(field_name="contract_type", lookup_expr="icontains")

    class Meta:
        model = Doctor
        fields = ["first_name", "father_name", "last_name", "email", "aca_degree", "contract_type"]