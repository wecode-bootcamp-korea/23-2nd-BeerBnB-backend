import jwt
import json

from django.test     import TestCase, Client

from users.models    import User
from products.models import Product
from .models         import Booking
from my_settings     import SECRET_KEY

class BookingTest(TestCase):
    def setUp(self):
        User.objects.bulk_create(
            [User(
                kakao     = 123456789,
                name      = "홍길동",
                birthday  = "2000-11-30",
                thumbnail = "http://yyy.kakao.com/.../img_110x110.jpg",
                is_host   = False),
            User(
                kakao     = 5555,
                name      = "박종규",
                birthday  = "2000-12-03",
                thumbnail = "http://yyy.kakao.com/.../img_110x110.jpg",
                is_host   = True)]
        )

        Product.objects.bulk_create(
            [Product(
                name           = "1호점",
                head_count     = 4,
                latitude       = 1,
                longitude      = 1,
                price          = 100,
                address        = "서울시 강남구",
                detail_address = "위워크",
                grade          = 0,
                description    = "추워요",
                user_id        = User.objects.get(kakao=5555).id),
            Product(
                name           = "2호점",
                head_count     = 4,
                latitude       = 2,
                longitude      = 2,
                price          = 100,
                address        = "서울시 강동구",
                detail_address = "위워크",
                grade          = 0,
                description    = "추워요",
                user_id        = User.objects.get(kakao = 5555).id)]
        )
        
    def tearDown(self):
        Booking.objects.all().delete()
        Product.objects.all().delete()
        User.objects.all().delete()
    
    def test_booking_success(self):
        user       = User.objects.get(kakao = 123456789)
        fake_token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm = "HS256")
        
        client     = Client()
        headers    = {"HTTP_Authorization" : fake_token}
        body       = {"checkin" : "2021-08-29", "checkout" : "2021-08-31", "count" : 4}
        product_id = Product.objects.get(name="1호점").id
        response   = client.post(f"/bookings/{product_id}", json.dumps(body), content_type = "application/json", **headers)
        self.assertEqual(response.status_code, 201)

    def test_booking_fail_key_error(self) :
        user       = User.objects.get(kakao = 123456789)
        fake_token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm = "HS256")
    
        client     = Client()
        headers    = {"HTTP_Authorization" : fake_token}
        body       = {"checkin" : "2021-08-29", "count" : 4}
        product_id = Product.objects.get(name = "1호점").id
        response   = client.post(f"/bookings/{product_id}", json.dumps(body), content_type = "application/json", **headers)
        self.assertEqual(response.status_code, 400)

    def test_booking_fail_no_product(self) :
        user       = User.objects.get(kakao = 123456789)
        fake_token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm = "HS256")
    
        client   = Client()
        headers  = {"HTTP_Authorization" : fake_token}
        body     = {"checkin" : "2021-08-29", "count" : 4}
        response = client.post(f"/bookings/1000", json.dumps(body), content_type = "application/json",**headers)
        self.assertEqual(response.status_code, 400)
        
class BookedProductGuestTest(TestCase):
    def setUp(self):
        User.objects.bulk_create(
            [User(
                kakao     = 123456789,
                name      = "홍길동",
                birthday  = "2000-11-30",
                thumbnail = "http://yyy.kakao.com/.../img_110x110.jpg",
                is_host   = False),
            User(
                kakao     = 5555,
                name      = "박종규",
                birthday  = "2000-12-03",
                thumbnail = "http://yyy.kakao.com/.../img_110x110.jpg",
                is_host   = True)]
        )
        
        Product.objects.bulk_create(
            [Product(
                name           = "1호점",
                head_count     = 4,
                latitude       = 1,
                longitude      = 1,
                price          = 100,
                address        = "서울시 강남구",
                detail_address = "위워크",
                grade          = 0,
                description    = "추워요",
                user_id        = User.objects.get(kakao = 5555).id),
            Product(
                name           = "2호점",
                head_count     = 4,
                latitude       = 2,
                longitude      = 2,
                price          = 100,
                address        = "서울시 강동구",
                detail_address = "위워크",
                grade          = 0,
                description    = "추워요",
                user_id        = User.objects.get(kakao = 5555).id)]
        )
        
        Booking.objects.create(
            check_in    = "2021-10-11",
            check_out   = "2021-10-14",
            head_count  = 4,
            total_price = 300,
            product_id  = Product.objects.get(name = "1호점").id,
            user_id     = User.objects.get(kakao = 123456789).id
        )
        
    def tearDown(self) :
        Booking.objects.all().delete()
        Product.objects.all().delete()
        User.objects.all().delete()
    
    def test_booked_product_guest_success(self):
        user       = User.objects.get(kakao = 123456789)
        fake_token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm = "HS256")
        
        client   = Client()
        headers  = {"HTTP_Authorization" : fake_token}
        response = client.get("/bookings/guest", **headers)
        self.assertEqual(response.status_code, 200)
    
    def test_booked_product_guest_no_item_success(self):
        user       = User.objects.get(kakao = 5555)
        fake_token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm = "HS256")
        
        client   = Client()
        headers  = {"HTTP_Authorization" : fake_token}
        response = client.get("/bookings/guest", **headers)
        self.assertEqual(response.json()["message"], [])

class BookedProductHostTest(TestCase):
    def setUp(self) :
        User.objects.bulk_create(
            [User(
                kakao     = 123456789,
                name      = "홍길동",
                birthday  = "2000-11-30",
                thumbnail = "http://yyy.kakao.com/.../img_110x110.jpg",
                is_host   = False),
                User(
                kakao     = 5555,
                name      = "박종규",
                birthday  = "2000-12-03",
                thumbnail = "http://yyy.kakao.com/.../img_110x110.jpg",
                is_host   = True)]
        )
        
        Product.objects.bulk_create(
            [Product(
                name           = "1호점",
                head_count     = 4,
                latitude       = 1,
                longitude      = 1,
                price          = 100,
                address        = "서울시 강남구",
                detail_address = "위워크",
                grade          = 0,
                description    = "추워요",
                user_id        = User.objects.get(kakao = 5555).id),
                Product(
                name = "2호점",
                head_count     = 4,
                latitude       = 2,
                longitude      = 2,
                price          = 100,
                address        = "서울시 강동구",
                detail_address = "위워크",
                grade          = 0,
                description    = "추워요",
                user_id        = User.objects.get(kakao = 5555).id)]
        )
        
        Booking.objects.create(
            check_in    = "2021-10-11",
            check_out   = "2021-10-14",
            head_count  = 4,
            total_price = 300,
            product_id  = Product.objects.get(name = "1호점").id,
            user_id     = User.objects.get(kakao = 123456789).id
        )
    
    def tearDown(self) :
        Booking.objects.all().delete()
        Product.objects.all().delete()
        User.objects.all().delete()
    
    def test_booked_product_host_success(self) :
        user       = User.objects.get(kakao = 5555)
        fake_token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm = "HS256")
        
        client   = Client()
        headers  = {"HTTP_Authorization" : fake_token}
        response = client.get("/bookings/host", **headers)
        self.assertEqual(response.status_code, 200)

    def test_booked_product_is_host_false_fail(self) :
        user       = User.objects.get(kakao = 123456789)
        fake_token = jwt.encode({"id" : user.id}, SECRET_KEY, algorithm = "HS256")
    
        client   = Client()
        headers  = {"HTTP_Authorization" : fake_token}
        response = client.get("/bookings/host", **headers)
        self.assertEqual(response.status_code, 400)