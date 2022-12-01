from django.urls import path

from . import views

urlpatterns = [
    path("watchlist_items", views.watchlist_items, name="watchlist_items"),
    path("listing_page/<int:auction_id>", views.listing_page, name="listing_page"),
    path("create_list", views.create_list, name="create_list"),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
    
]
