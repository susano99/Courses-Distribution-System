from django.contrib import admin
from management import models


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["id", "code", "language", "is_elective"]
    search_fields = ["id", "code", "language", "is_elective"]


admin.site.register(models.Registration)
