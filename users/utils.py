import jwt

from django.http import JsonResponse

from BeerBnB.settings import SECRET_KEY
from .models          import User


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token   = request.headers.get("Authorization")
            payload = jwt.decode(token, SECRET_KEY, algorithms = "HS256")

            if not User.objects.filter(id = payload.get("id")).exists() :
                return JsonResponse({"message" : "INVALID_MEMBER"}, status = 404)

            user         = User.objects.get(id = payload["id"])
            request.user = user

            return func(self, request, *args, **kwargs)
        
        except jwt.exceptions.DecodeError:
            return JsonResponse({"message" : "INVALID_TOKEN"}, status = 403)

    return wrapper
