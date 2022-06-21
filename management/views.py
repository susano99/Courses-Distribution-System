from django.db import DatabaseError
from django.shortcuts import render
from rest_framework import mixins, serializers, viewsets
from accounts.models import Doctor
from management.models import Course, Registration
from django.db.models import Sum
from commons.mixins import StaffEditorPermissionMixin
from .filters import CourseFilter, RegistrationFilter


class CoursesViewSet(
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet,):

    def get_queryset(self):
        ordering = self.request.query_params.get("ordering", None)
        queryset = Course.objects.all()
        if ordering:
            try:
                queryset = queryset.order_by(ordering)
            except:
                pass
        if "elective" in self.request.query_params:
            queryset = queryset.filter(is_elective=True)
        return queryset
    
    filter_class = CourseFilter

    class CoursesSerializer(serializers.ModelSerializer):
        class Meta:
            model = Course
            fields = '__all__'

    class CreateCourseSerializer(serializers.Serializer):
        code = serializers.CharField(max_length=128)
        language = serializers.CharField(max_length=128)
        name = serializers.CharField(max_length=128)
        is_elective = serializers.BooleanField(default=False)
        semester = serializers.CharField(max_length=128)
        full_hours = serializers.IntegerField()
        course_hours = serializers.IntegerField()
        tp_hours = serializers.IntegerField()
        td_hours = serializers.IntegerField()
        nbr_of_credits = serializers.IntegerField()
        department = serializers.CharField(max_length=128)
        description = serializers.CharField(required=False, max_length=128)
        major = serializers.CharField(max_length=128)
        is_archived = serializers.BooleanField(default=False)

        def validate(self, data):
            sum_fields = data['course_hours'] + \
                data['tp_hours'] + data['td_hours']
            if Course.objects.filter(code=data['code'], language=data['language'].lower()):
                raise serializers.ValidationError('Course already exists.')
            if sum_fields > data['full_hours']:
                raise serializers.ValidationError(
                    "Fields sum can't exceed full hours.")
            return data

    class UpdateCourseSerializer(serializers.Serializer):
        code = serializers.CharField(required=False, max_length=128)
        name = serializers.CharField(required=False, max_length=128)
        is_elective = serializers.BooleanField(default=False)
        semester = serializers.CharField(required=False, max_length=128)
        full_hours = serializers.IntegerField(required=False,)
        course_hours = serializers.IntegerField(required=False,)
        tp_hours = serializers.IntegerField(required=False,)
        td_hours = serializers.IntegerField(required=False,)
        nbr_of_credits = serializers.IntegerField(required=False,)
        department = serializers.CharField(required=False, max_length=128)
        description = serializers.CharField(required=False, max_length=128)
        major = serializers.CharField(required=False, max_length=128)
        is_archived = serializers.BooleanField(default=False)

    def get_serializer_class(self):
        if self.action == "create":
            return self.CreateCourseSerializer
        if self.action == "update":
            return self.UpdateCourseSerializer
        return self.CoursesSerializer

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        Course.objects.create(
            code=serializer.validated_data.get('code'),
            language=serializer.validated_data.get('language'),
            name=serializer.validated_data.get('name'),
            is_elective=serializer.validated_data.get('is_elective'),
            semester=serializer.validated_data.get('semester'),
            full_hours=serializer.validated_data.get('full_hours'),
            course_hours=serializer.validated_data.get('course_hours'),
            tp_hours=serializer.validated_data.get('tp_hours'),
            td_hours=serializer.validated_data.get('td_hours'),
            nbr_of_credits=serializer.validated_data.get('nbr_of_credits'),
            department=serializer.validated_data.get('department'),
            description=serializer.validated_data.get('description'),
            major=serializer.validated_data.get('major'),
            is_archived=serializer.validated_data.get('is_archived'),
        )

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        course = self.get_object()
        course.code = serializer.validated_data.get('code', course.code)
        course.name = serializer.validated_data.get('name', course.name)
        course.is_elective = serializer.validated_data.get(
            'is_elective', course.is_elective)
        course.semester = serializer.validated_data.get(
            'semester', course.semester)
        course.full_hours = serializer.validated_data.get(
            'full_hours', course.full_hours)
        course.course_hours = serializer.validated_data.get(
            'course_hours', course.course_hours)
        course.tp_hours = serializer.validated_data.get(
            'tp_hours', course.tp_hours)
        course.td_hours = serializer.validated_data.get(
            'td_hours', course.td_hours)
        course.nbr_of_credits = serializer.validated_data.get(
            'nbr_of_credits', course.nbr_of_credits)
        course.department = serializer.validated_data.get(
            'department', course.department)
        course.description = serializer.validated_data.get(
            'description', course.description)
        course.major = serializer.validated_data.get('major', course.major)
        course.is_archived = serializer.validated_data.get(
            'is_archived', course.is_archived)
        course.save()


class RegistrationViewSet(
        StaffEditorPermissionMixin,
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet,):

    queryset = Registration.objects.all()
    filter_class = RegistrationFilter

    class RegistrationsSerializer(serializers.ModelSerializer):
        class Meta:
            model = Registration
            fields = "__all__"

    class CreateRegistrationSerializer(serializers.Serializer):
        doctor = serializers.PrimaryKeyRelatedField(
            queryset=Doctor.objects.all())
        course = serializers.PrimaryKeyRelatedField(
            queryset=Course.objects.all())
        course_hours = serializers.IntegerField()
        tp_hours = serializers.IntegerField()
        td_hours = serializers.IntegerField()
        year = serializers.CharField(max_length=128)

        def validate(self, data):
            sum = Registration.objects.filter(
                course=1, year='2019-2020').aggregate(Sum('tp_hours'), Sum('course_hours'), Sum('td_hours'))
            course_available = Course.detect_course(data['course'])
            if Registration.objects.filter(course=data["course"], doctor=data["doctor"], year=data["year"]):
                raise serializers.ValidationError("Already Distributed")
            if sum['course_hours__sum'] + data['course_hours'] > course_available.course_hours:
                raise serializers.ValidationError("Exceeded Course hours.")
            if sum['tp_hours__sum'] + data['tp_hours'] > course_available.tp_hours:
                raise serializers.ValidationError("Exceeded tp hours hours.")
            if sum['td_hours__sum'] + data['td_hours'] > course_available.td_hours:
                raise serializers.ValidationError("Exceeded td hours hours.")
            return data

    class UpdateRegistrationSerializer(serializers.Serializer):
        doctor = serializers.PrimaryKeyRelatedField(
            required=False, queryset=Doctor.objects.all())
        course_hours = serializers.IntegerField(required=False, )
        tp_hours = serializers.IntegerField(required=False, )
        td_hours = serializers.IntegerField(required=False, )
        year = serializers.CharField(required=False, max_length=128)

        def validate(self, data):
            sum = Registration.objects.filter(
                course=1, year='2019-2020').aggregate(Sum('tp_hours'), Sum('course_hours'), Sum('td_hours'))
            course_available = Course.detect_course(data['course'])
            if Registration.objects.filter(course=data["course"], doctor=data["doctor"], year=data["year"]):
                raise serializers.ValidationError("Already Distributed")
            if sum['course_hours'] + data['course_hours'] > course_available.course_hours:
                raise serializers.ValidationError("Exceeded Course hours.")
            if sum['tp_hours__sum'] + data['tp_hours'] > course_available.tp_hours:
                raise serializers.ValidationError("Exceeded tp hours hours.")
            if sum['td_hours__sum'] + data['td_hours'] > course_available.td_hours:
                raise serializers.ValidationError("Exceeded td hours hours.")
            return data

    def get_serializer_class(self):
        if self.action == "create":
            return self.CreateRegistrationSerializer
        if self.action == "update":
            return self.UpdateRegistrationSerializer
        return self.RegistrationsSerializer

    def calculate_section(self, crs_id):
        i = 1
        count = Registration.objects.filter(course_id=crs_id).count()
        print(count)
        qs = Registration.objects.filter(
            course_id=crs_id).order_by('created_at')
        if count > 1:
            for obj in qs.iterator():
                obj.section = f'{i}/{count}'
                obj.save()
                i = i + 1
        elif count == 1:
            for obj in qs.iterator():
                obj.section = "1/1"
                obj.save()

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        register = Registration.objects.create(
            doctor=serializer.validated_data.get('doctor'),
            course=serializer.validated_data.get('course'),
            course_hours=serializer.validated_data.get('course_hours'),
            tp_hours=serializer.validated_data.get('tp_hours'),
            td_hours=serializer.validated_data.get('td_hours'),
            year=serializer.validated_data.get('year'),
        )
        self.calculate_section(register.course_id)

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        registration = self.get_object()
        registration.doctor = serializer.validated_data.get(
            'doctor', registration.doctor)
        registration.course_hours = serializer.validated_data.get(
            'course_hours', registration.course_hours)
        registration.tp_hours = serializer.validated_data.get(
            'tp_hours', registration.tp_hours)
        registration.td_hours = serializer.validated_data.get(
            'td_hours', registration.td_hours)
        registration.year = serializer.validated_data.get(
            'year', registration.year)
        registration.save()

    def perform_destroy(self, instance):
        crs_id = instance.course_id
        instance.delete()
        self.calculate_section(crs_id)
