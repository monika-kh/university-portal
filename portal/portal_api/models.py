import uuid
from django.contrib.auth.models import User, AbstractBaseUser
from django.db import models


class CustomeUser(AbstractBaseUser):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    university_id = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)
    uuid_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_dean = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    USERNAME_FIELD = "university_id"

    def __str__(self):
        return f"{self.user.username}"


class DeansSessionAvailability(models.Model):
    dean = models.ForeignKey(
        CustomeUser, on_delete=models.CASCADE, related_name="dean_availability"
    )
    session_status = models.CharField(max_length=10, default="Free")
    session_date = models.DateTimeField()
    is_pending = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.dean.user.username} - {self.session_status} - {self.session_date.date()}"


class StudentBookedSession(models.Model):
    student = models.ForeignKey(
        CustomeUser, related_name="booked_sessions", on_delete=models.CASCADE
    )
    session = models.ForeignKey(
        DeansSessionAvailability,
        related_name="student_session",
        on_delete=models.CASCADE,
    )
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.username} - {self.session.session_date.date()}"
