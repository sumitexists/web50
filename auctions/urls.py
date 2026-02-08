from django.urls import path

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("NewListing/", views.create_listing ,  name = 'new_listing'),
    path("Listing/<int:listing_id>", views.listing, name="listing"),
    path("Watchlist/", views.watchlist ,name = "watchlist"),
    path("Categories/", views.categories , name = "categories")
]
