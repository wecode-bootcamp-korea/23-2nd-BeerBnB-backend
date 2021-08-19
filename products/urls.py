from django.urls    import path

from products.views import ProductsListView

urlpatterns = [
    path("",ProductsListView.as_view()),
]
