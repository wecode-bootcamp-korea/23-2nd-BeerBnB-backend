import json
from datetime         import datetime

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from .models          import Booking
from products.models  import Product
from users.utils      import login_decorator

class BookingView(View):
    @login_decorator
    def post(self, request, product_id):
        try:
            data        = json.loads(request.body)
            
            check_in    = data["checkin"]
            check_out   = data["checkout"]
            head_count  = data["count"]
            
            if not check_in or not check_out or not head_count:
                raise KeyError
            
            start_date = datetime.strptime(check_in, "%Y-%m-%d")
            end_date   = datetime.strptime(check_out, "%Y-%m-%d")
            
            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({"message": "NO_PRODUCT"}, status = 400)
            
            price       = Product.objects.get(id=product_id).price
            total_price = price * (end_date - start_date).days
            
            Booking.objects.create(
                user_id     = request.user.id,
                product_id  = product_id,
                check_in    = check_in,
                check_out   = check_out,
                head_count  = head_count,
                total_price = total_price
            )
            
            return JsonResponse({"message": "BOOKED"}, status = 201)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)

class BookedProductsGuestView(View):
    @login_decorator
    def get(self, request):
        today  = datetime.today()
        booked = Booking.objects.filter(Q(user = request.user.id) & Q(check_out__gte = today)).select_related("product")
            
        products = [{
            "booking_id"   : booking.id,
            "product_id"   : booking.product.id,
            "product_name" : booking.product.name,
            "check_in"     : booking.check_in,
            "check_out"    : booking.check_out,
            "total_price"  : booking.total_price
            } for booking in booked]
        
        return JsonResponse({"message" : products}, status = 200)


class BookedProductsHostView(View) :
    @login_decorator
    def get(self, request) :
        if not request.user.is_host:
            return JsonResponse({"message" : "USER_IS_NOT_HOST"}, status = 400)

        today  = datetime.today()
        booked = Booking.objects.filter(Q(product__user_id = request.user.id) & Q(check_out__gte = today)).select_related("product", "user")
        
        products = [{
            "booking_id"         : booking.id,
            "booking_user_name"  : booking.user.name,
            "booking_created_at" : booking.created_at,
            "product_id"         : booking.product.id,
            "product_name"       : booking.product.name,
            "check_in"           : booking.check_in,
            "check_out"          : booking.check_out,
            "total_price"        : booking.total_price
        } for booking in booked]
        
        return JsonResponse({"message" : products}, status = 200)