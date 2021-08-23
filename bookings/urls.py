from django.urls import path
from .views      import BookingView, BookedProductsGuestView, BookedProductsHostView

urlpatterns = [
    path("/<int:product_id>", BookingView.as_view()),
    path("/guest", BookedProductsGuestView.as_view()),
    path("/host", BookedProductsHostView.as_view())
]
