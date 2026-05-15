from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("",views.home,name="home"),
    path("productlisting",views.product_listing,name="product_listing"),
    path("productdetails/<int:myid>",views.product_details,name="product_details"),
    path("search",views.search,name="search"),
    path("signup",views.submit_signup,name="submit_signup"),
    path("login",views.submit_login,name="login"),
    path("logout",views.submit_logout,name="logout"),
    path("about",views.about,name="about")
]












