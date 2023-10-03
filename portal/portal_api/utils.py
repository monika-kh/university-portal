from .models import CustomeUser


def get_token(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    if not token:
        return None

    _, uuid_token = token.split()
    user = CustomeUser.objects.filter(uuid_token=uuid_token)
    return user
