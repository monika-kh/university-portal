from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from portal_api.permissions import IsDean, IsStudent
from portal_api.utils import get_token
from .models import CustomeUser, StudentBookedSession, DeansSessionAvailability
from .serializers import (
    UserSerializer,
    PendingSessionSerializer,
    DeansSessionAvailabilitySerializer,
    StudentBookedSessionSerializer,
)
import uuid


class LoginAPI(APIView):
    def post(self, request):
        university_id = request.data.get("university_id")
        password = request.data.get("password")

        try:
            user = CustomeUser.objects.get(university_id=university_id)

            if password == user.password:
                user.uuid_token = str(uuid.uuid4()).replace("-", "")

                user.save()

                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomeUser.DoesNotExist:
            pass
        return Response(
            {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class SessionBookedByStudent(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        """
        Get all the free available sessions of the deans in the university.
        """
        free_sessions = DeansSessionAvailability.objects.filter(
            session_status="Free", session_date__gte=datetime.now()
        ).order_by("dean")

        dean_sessions = {}
        for session in free_sessions:
            dean = session.dean
            if dean not in dean_sessions:
                dean_sessions[dean] = []
            dean_sessions[dean].append(session)

        serialized_data = {}
        for dean, sessions in dean_sessions.items():
            serializer = DeansSessionAvailabilitySerializer(sessions, many=True)
            serialized_data[dean.user.username] = serializer.data

        return Response(serialized_data, status=status.HTTP_200_OK)

    def post(self, request, pk=None):
        """
        Student can book the Session by selecting the slot of the dean by selecting the slot id.
        """

        student = get_token(request)
        session = DeansSessionAvailability.objects.get(id=pk)
        copy_data = request.data.copy()
        copy_data["student"] = student[0].id
        copy_data["session"] = session.id
        if not StudentBookedSession.objects.filter(
            session=session.id, student=student[0].id
        ):
            serializer = StudentBookedSessionSerializer(data=copy_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Slot already booked"})


class GetDeanPendingSession(APIView):

    """
    Dean can check the pending session with the list of student names who booked that particular pennding session.
    """

    permission_classes = [IsDean]

    def get(self, request):
        dean = get_token(request)
        if dean.exists() and (dean[0].is_dean):
            if "pending-session-details" in request.path:
                sessions = DeansSessionAvailability.objects.filter(
                    dean=dean[0].id, is_pending=True, session_date__lte=datetime.now()
                )
            else:
                sessions = DeansSessionAvailability.objects.filter(
                    dean=dean[0].id, is_pending=True, session_date__gte=datetime.now()
                )

            sessions_data = []

            for session in sessions:
                booked_sessions = StudentBookedSession.objects.filter(
                    session=session, is_booked=True
                )

                students_data = PendingSessionSerializer(
                    booked_sessions.values("student__user__username"), many=True
                ).data

                session_data = {
                    "session_id": session.id,
                    "dean": session.dean.user.username,
                    "session_status": session.session_status,
                    "session_date": session.session_date,
                    "students": students_data,
                }

                sessions_data.append(session_data)

            return Response(sessions_data, status=status.HTTP_200_OK)
        return Response({"detail": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
