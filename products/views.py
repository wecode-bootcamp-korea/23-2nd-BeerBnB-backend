from datetime         import datetime, timedelta

from django.views     import View
from django.db.models import Q, Prefetch
from django.http      import JsonResponse

from products.models  import Product

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