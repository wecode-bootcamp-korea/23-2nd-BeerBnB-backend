import json
import jwt

from django.http       import response
from django.test       import TestCase, Client
from django.test.utils import teardown_databases

from .models           import Product,Image,Category
from BeerBnB.settings  import SECRET_KEY
from users.models      import User
from bookings.models   import Booking

class ProductListTest(TestCase):
    def setUp(self):
        User.objects.bulk_create(
            [User(
                kakao     = 1234,
                name      = "박종규",
                thumbnail = "photo1",
                birthday  = "2000-12-03",
                is_host   = True),
                User(
                kakao     = 7777,
                name      = "방문객",
                thumbnail = "photo2",
                birthday  = "2000-12-04",
                is_host   = False)]
        )
        
        Product.objects.bulk_create(
            [Product(
                name           = "1호집",
                head_count     = 4,
                latitude       = 1,
                longitude      = 1,
                price          = 100,
                address        = "서울시 강남구",
                detail_address = "1002호",
                grade          = 0,
                description    = "좋아요",
                user_id        = User.objects.get(kakao=1234).id),
                Product(
                name           = "2호집",
                head_count     = 2,
                latitude       = 1,
                longitude      = 1,
                price          = 100,
                address        = "서울시 강동구",
                detail_address = "1003호",
                grade          = 0,
                description    = "좋아요",
                user_id        = User.objects.get(kakao=1234).id)]
        )
        
        Image.objects.bulk_create(
            [Image(product_id = Product.objects.get(name="1호집").id, image = "1호점 사진1"),
             Image(product_id = Product.objects.get(name="1호집").id, image = "1호점 사진2"),
             Image(product_id = Product.objects.get(name="2호집").id, image = "2호점 사진1")])

        Category.objects.bulk_create(
            [Category(
                product_id    = Product.objects.get(name="1호집").id,
                big_address   = "서울시",
                small_address = "강남구"),
                Category(
                product_id    = Product.objects.get(name="2호집").id,
                big_address   = "서울시",
                small_address = "강동구")]
        )

        Booking.objects.create(
            product_id  = Product.objects.get(name="1호집").id,
            user_id     = User.objects.get(kakao=7777).id,
            check_in    = "2021-08-29",
            check_out   = "2021-08-31",
            head_count  = 1,
            total_price = 100
        )
    
    def tearDown(self):
        Booking.objects.all().delete()
        Image.objects.all().delete()
        Category.objects.all().delete()
        Product.objects.all().delete()
        User.objects.all().delete()
        
    def test_search_success(self):
        client   = Client()
        response = client.get("/products?address=서울시 강남구&checkin=2021-08-20&checkout=2021-08-21&count=3")
        self.assertEqual(response.status_code, 200)

    def test_search_success_without_address(self) :
        client   = Client()
        response = client.get("/products?checkin=2021-08-20&checkout=2021-08-21&count=4")
        self.assertEqual(response.status_code, 200)

    def test_search_success_overheadcount(self):
        client   = Client()
        response = client.get("/products?address=서울시&checkin=2021-08-20&checkout=2021-08-21&count=5")
        self.assertEqual(response.json()["message"], [])
        
    def test_search_fail_without_checkout(self):
        client   = Client()
        response = client.get("/products?address=서울시&checkin=2021-08-20&count=3")
        self.assertEqual(response.json()["message"], "NEED_DATE")
        
    def test_search_fail_valueerror(self):
        client   = Client()
        response = client.get("/products?address=서울시&checkin=2021-08-20&checkout=rrr&count=3")
        self.assertEqual(response.json()["message"], "VALUE_ERROR")
        
class HostTest(TestCase):
    def setUp(self):  
        user = User.objects.create(
            kakao     = 123425,
            name      = "dodam",
            birthday  = "2000-01-01",
            thumbnail = "http://img.url",
            is_host   = False,
        )

        product = Product.objects.create(
            user_id        = User.objects.get(kakao=123425).id,
            name           = "오션뷰 최고",
            head_count     = 4,
            price          = 20000,
            latitude       = 34.12345678,
            longitude      = 25.564678,
            description    = "편하고 아늑한 방",
            grade          = 0,
            address        = "강원도 강릉시",
            detail_address = "안목카페거리",
            )

        Image.objects.bulk_create(
            [Image(
                product_id = Product.objects.get(name="오션뷰 최고").id, 
                image      = "url" )]
        ) 

        Category.objects.create(
            product_id    = Product.objects.get(name="오션뷰 최고").id,
            big_address   = product.address.split(" ")[0],
            small_address = product.address.split(" ")[1],
        )

        self.token = jwt.encode({"id" : User.objects.get(kakao=123425).id}, SECRET_KEY, algorithm = "HS256")

    def tearDown(self):
        User.objects.all().delete()
        Product.objects.all().delete()
        Image.objects.all().delete()
        Category.objects.all().delete()

    def test_host_success(self):
        client   = Client()
        headers  = {'HTTP_Authorization' : self.token}
        
        product = { 
                "user"           : User.objects.get(kakao=123425).id,
                "name"           : "오션뷰 최고",
                "head_count"     : 4,
                "price"          : 20000,
                "latitude"       : 34.123456,
                "longitude"      : 25.564678,
                "description"    : "편하고 아늑한 방",
                "address"        : "강원도 강릉시",
                "detail_address" : "안목카페거리"  ,
                "grade"          : 0,    
                "image"          : "123",       
            }
        
        response = client.post('/products/post', json.dumps(product),content_type='application/json',**headers) 

        self.assertEqual(response.status_code, 200)     
        self.assertEqual(response.json(), 
            {
                'MESSAGE' : 'SUCCESS'
            }
        )
