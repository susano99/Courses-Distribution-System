from django.contrib import admin
from accounts import models


@admin.register(models.Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "father_name", "last_name", "phone",
                    "email", "phone", "email", "aca_degree", "contract_type", "is_archived"]
    search_fields = ["id", "first_name", "father_name", "last_name", "phone",
                     "email", "phone", "email", "aca_degree", "contract_type", "is_archived"]
