from django.urls    import path
from products.views import ProductsListView, Host, DetailView

urlpatterns = [
    path("", ProductsListView.as_view()),
    path("/post", Host.as_view()),
    path('/<int:product_id>', DetailView.as_view()),
]