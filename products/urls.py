from django.urls    import path
from products.views import ProductsListView, Host

urlpatterns = [
    path("",ProductsListView.as_view()),
    path("/post", Host.as_view()),
]


