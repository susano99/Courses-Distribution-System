from rest_framework import mixins, serializers, status, viewsets
from rest_framework.response import Response
from accounts.models import Doctor
from django.contrib.auth.models import User
from commons.mixins import StaffEditorPermissionMixin
from .filters import DoctorFilter


class DoctorsViewSet(
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):

    queryset = Doctor.objects.all()
    filter_class = DoctorFilter

    class DoctorsSerializer(serializers.ModelSerializer):
        class Meta:
            model = Doctor
            fields = "__all__"

    class CreateDoctorsSerializer(serializers.Serializer):
        first_name = serializers.CharField(max_length=128)
        father_name = serializers.CharField(max_length=128)
        last_name = serializers.CharField(max_length=128)
        phone = serializers.IntegerField(required=False)
        email = serializers.EmailField(required=False)
        aca_degree = serializers.CharField(
            max_length=128, required=False)
        contract_type = serializers.CharField(
            max_length=128, required=False)
        is_archived = serializers.BooleanField(default=False)

    class UpdateDoctorsSerializer(serializers.Serializer):
        first_name = serializers.CharField(max_length=128, required=False)
        father_name = serializers.CharField(max_length=128, required=False)
        last_name = serializers.CharField(max_length=128, required=False)
        phone = serializers.IntegerField(required=False)
        email = serializers.EmailField(required=False)
        aca_degree = serializers.CharField(
            max_length=128, required=False)
        contract_type = serializers.CharField(
            max_length=128, required=False)
        is_archived = serializers.BooleanField(default=False)

    def get_serializer_class(self):
        if self.action == "create":
            return self.CreateDoctorsSerializer
        if self.action == "update":
            return self.UpdateDoctorsSerializer
        return self.DoctorsSerializer

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        Doctor.objects.create(
            first_name=serializer.validated_data.get("first_name"),
            father_name=serializer.validated_data.get("father_name"),
            last_name=serializer.validated_data.get("last_name"),
            phone=serializer.validated_data.get("phone"),
            email=serializer.validated_data.get("email"),
            aca_degree=serializer.validated_data.get("aca_degree"),
            contract_type=serializer.validated_data.get("contract_type"),
            is_archived=serializer.validated_data.get("is_archived")
        )

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        doctor = self.get_object()
        doctor.first_name = serializer.validated_data.get(
            "first_name", doctor.first_name)
        doctor.father_name = serializer.validated_data.get(
            "father_name", doctor.father_name)
        doctor.last_name = serializer.validated_data.get(
            "last_name", doctor.last_name)
        doctor.phone = serializer.validated_data.get("phone", doctor.phone)
        doctor.email = serializer.validated_data.get("email", doctor.email)
        doctor.aca_degree = serializer.validated_data.get(
            "aca_degree", doctor.aca_degree)
        doctor.contract_type = serializer.validated_data.get(
            "contract_type", doctor.contract_type)
        doctor.is_archived = serializer.validated_data.get(
            "is_archived", doctor.is_archived)
        doctor.save()