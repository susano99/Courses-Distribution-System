from django.db import models
from commons.models import AbstractModel
from accounts.models import Doctor


class Course(models.Model):
    code = models.CharField(max_length=128)
    language = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    is_elective = models.BooleanField(default=False)
    semester = models.CharField(max_length=128)
    full_hours = models.IntegerField()
    course_hours = models.IntegerField()
    tp_hours = models.IntegerField()
    td_hours = models.IntegerField()
    nbr_of_credits = models.IntegerField()
    department = models.CharField(max_length=128)
    description = models.CharField(max_length=128, blank=True, null=True)
    major = models.CharField(max_length=128)
    is_archived = models.BooleanField(default=False)

    def archive(self):
        if not self.is_archived:
            self.is_archived = True
            self.save()

    def unarchive(self):
        if self.is_archived:
            self.is_archived = False
            self.save()

    @classmethod
    def detect_course(self, text):
        try:
            course = self.objects.get(code=text)
            return course
        except:
            pass

        try:
            course = self.objects.get(id=text)
            return course
        except:
            pass
        return None

    def __str__(self):
        return self.code


class Registration(AbstractModel):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="registrations")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="registrations")
    course_hours = models.IntegerField()
    tp_hours = models.IntegerField()
    td_hours = models.IntegerField()
    section = models.CharField(
        max_length=128, blank=True, null=True, default="1/1")
    year = models.CharField(max_length=128)
