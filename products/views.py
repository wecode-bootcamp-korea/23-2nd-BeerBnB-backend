import json
from datetime         import datetime, timedelta

from django.http      import JsonResponse, request
from django.views     import View
from django.db        import transaction
from django.db.models import Q, Prefetch

from products.models  import Product, Image, Category
from bookings.models import Booking
from users.models     import User
from users.utils      import login_decorator

class ProductsListView(View):
    def get(self, request):
        try:
            # 주소 검색
            address  = request.GET.get("address")
            
            q = Q()
            
            if address:
                q &= Q(address__contains=address)
            
            address_filtered_products = Product.objects.filter(q)
    
            # 날짜 검색
            checkin  = request.GET.get("checkin")
            checkout = request.GET.get("checkout")
            
            if not checkin or not checkout:
                return JsonResponse({"message" : "NEED_DATE"}, status = 400)
            
            new_checkout = datetime.strptime(checkout, "%Y-%m-%d").date() - timedelta(1)
            
            date_filtered_products = address_filtered_products.exclude(
                (Q(booking__check_out__gt = checkin) & Q(booking__check_in__lte = checkin)) |
                Q(booking__check_in__range = [checkin, new_checkout])
            )
            
            # 인원 가능 검색
            count = request.GET.get("count", 1)
            
            filtered_products = date_filtered_products.filter(head_count__gte = count).prefetch_related("image_set")
            
            products = [{
                "id"        : product.id,
                "name"      : product.name,
                "count"     : product.head_count,
                "latitude"  : product.latitude,
                "longitude" : product.longitude,
                "price"     : product.price,
                "image"     : [product.image for product in product.image_set.all()]
            } for product in filtered_products]
            
            return JsonResponse({"message" : products}, status = 200)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
        
        except ValueError:
            return JsonResponse({"message" : "VALUE_ERROR"}, status = 400)     

class Host(View):
    @login_decorator 
    @transaction.atomic   
    def post(self,request):
        data = json.loads(request.body)
        user = request.user

        if data["name"] == "" or data["head_count"] == "" or data["price"] == "":
          return JsonResponse ({"MESSAGE": "REQUIRE_INFORM_NULL"}, status = 400)

        MAX_PEOPLE = 5
        if data["head_count"] >= MAX_PEOPLE :
            return JsonResponse ({"MESSAGE":"PEOPLE_INPUT_ERROR"})   

        product = Product.objects.create(
            user_id        = user.id, 
            name           = data["name"],
            head_count     = data["head_count"],
            price          = data["price"],
            latitude       = data["latitude"],
            longitude      = data["longitude"],
            description    = data["description"],
            address        = data["address"],
            detail_address = data["detail_address"],
          )

        for image_id in data["image"]:
            Image.objects.create(product = product, image = data["image"])

        Category.objects.create(
            product       = product,
            big_address   = product.address.split(" ")[0],
            small_address = product.address.split(" ")[1],
        )
        
        if not data["image"]: 
            return JsonResponse({"MESSAGE": "IMAGE_DOES_NOT_EXISTS" },status = 400)

        if not data["address"] or not data["detail_address"] : 
            return JsonResponse({"MESSAGE": "ADDRESS_DOES_NOT_EXISTS" },status = 400)   

        if User.objects.filter(is_host=False).update(is_host=True) : 
            return JsonResponse ({"MESSAGE" : "SUCCESS"}, status = 200)

class DetailView(View):
    def get(self,request, product_id):
    
        if not Product.objects.filter(id=product_id).exists():
            return JsonResponse({"MESSAGE": "ROOM_DOES_NOT_EXISTS"},status = 400)

        product = Product.objects.get(id=product_id)
        booking = Booking.objects.get(id=product_id)

        response = {
            "id"             : product.id,
            "name"           : product.name,
            "head_count"     : product.head_count,
            "latitude"       : product.latitude,
            "longitude"      : product.longitude,
            "price"          : product.price,
            "address"        : product.address,
            "detail_address" : product.detail_address,
            "grade"          : product.grade,
            "description"    : product.description,
            "image"          : [product.image for product in product.image_set.all()],
            "check_in"       : booking.check_in,
            "check_out"      : booking.check_out,
            "host_name"      : product.user.name,
            "host_thumbnail" : product.user.thumbnail,
        }  

        return JsonResponse({"response":response}, status = 200)  
