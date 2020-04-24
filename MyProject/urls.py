from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Ecommerce import views
from django.contrib.auth import views as authviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup ,name='signup'),
    path('login/', authviews.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', authviews.LogoutView.as_view(), name='logout'),
    path('products/' , views.productList , name='productList' ),
    path('products/<int:id>/', views.productDetails , name='productDetails'),
    path('featured/' , views.featuredList , name='featuredList'),
    path('featured/<int:id>/' , views.featuredDetails , name='featuredDetails'),
    path('search/' , views.searchposts , name='search'),
    path('cart/' , views.cart , name='cart'),
    path('cart/cart-update', views.cartUpdate , name='cartUpdate'),
    path('cart/cart-update/checkout' , views.checkout , name='checkout')
   

]
#   +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns= urlpatterns + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
    urlpatterns= urlpatterns + static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)