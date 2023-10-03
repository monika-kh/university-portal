from django.urls import path
from .views import LoginAPI, GetDeanPendingSession, SessionBookedByStudent

urlpatterns = [
    path("login/", LoginAPI.as_view(), name="login"),
    path("get-session/", SessionBookedByStudent.as_view(), name="get-session"),
    path(
        "book-session/<int:pk>/", SessionBookedByStudent.as_view(), name="book-session"
    ),
    path(
        "pending-session-details/",
        GetDeanPendingSession.as_view(),
        name="session-details",
    ),
    path(
        "upcomming-session-details/",
        GetDeanPendingSession.as_view(),
        name="session-details",
    ),
]
