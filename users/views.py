import json
import jwt
import requests
from datetime     import datetime

from django.http  import JsonResponse
from django.views import View

from .models     import User
from my_settings import SECRET_KEY

class KakaoSigninView(View):
    def get(self, request):
        try:
            access_token = request.headers.get("Authorization")

            if not access_token:
                return JsonResponse({"message" : "NEED_TOKEN"}, status = 400)

            response = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers = {"Authorization" : f"Bearer {access_token}"},
                timeout = 5
            )
            
            if not response.status_code == 200:
                raise ConnectionError
            
            profile_json  = response.json()

            kakao_id      = profile_json.get("id")
            kakao_account = profile_json.get("kakao_account")
            name          = kakao_account["profile"]["nickname"]
            thumbnail     = kakao_account["profile"]["thumbnail_image_url"]
            month         = kakao_account["birthday"][0:2]
            day           = kakao_account["birthday"][2:4]
            birthday      = datetime.strptime(f"2000-{month}-{day}", "%Y-%m-%d").date() if kakao_account["birthday_needs_agreement"] else None

            user, created = User.objects.get_or_create(
                kakao     = kakao_id,
                defaults  = {
                    "name"      : name,
                    "thumbnail" : thumbnail,
                    "birthday"  : birthday,
                    "is_host"   : False
            })
            
            user.name      = name
            user.thumbnail = thumbnail
            user.birthday  = birthday
            user.save()

            token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm = "HS256")
            return JsonResponse({"message" : "SUCCESS", "token" : token}, status = 200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
        
        except ConnectionError:
            return JsonResponse({"message" : "KAKAO_ERROR"}, status = 408)