from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Ecommerce import views
from django.contrib.auth import views as authviews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    # path('signup/', views.signup ,name='signup'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup/login/', authviews.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', authviews.LogoutView.as_view(), name='logout'),
    path('products/' , views.productList , name='productList' ),
    path('products/<int:id>/', views.productDetails , name='productDetails'),
    path('featured/' , views.featuredList , name='featuredList'),
    path('featured/<int:id>/' , views.featuredDetails , name='featuredDetails'),
    path('search/' , views.searchproduct , name='search'),
    path('cart/' , views.cart , name='cart'),
    path('cart/checkout' , views.checkout , name='checkout'),
    path('cart/checkout/success' , views.success , name='success'),
    path('ajax/cart/delete/',  views.cartdelete.as_view(), name='cartDelete'),
    path('ajax/cart/login/',  views.cartlogin.as_view(), name='cartLogin'),
    path('ajax/cart/update/',  views.cartupdate.as_view(), name='cartUpdate'),
    path('ajax/cart/updateUser/',  views.updateUser.as_view(), name='updateUser'),
    path('ajax/order/' , views.order.as_view(), name='ajaxOrder'),
    path('ajax/product/review' , views.review.as_view(), name='ajaxReview'),
    path('ajax/user/signin' , views.loginUser.as_view(), name='ajaxsignin'),
    path('test/' , views.test , name='test'),
    path('login-signup' , views.loginSignup , name='login-signup'),
    path('user/profile' , views.profile ,name='user-profile'),
    path('order/details/<int:id>' , views.orderdetails ,name='user-detail'),


    

]
#   +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns= urlpatterns + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
    urlpatterns= urlpatterns + static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)