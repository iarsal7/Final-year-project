from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Ecommerce import views
from django.contrib.auth import views as authviews



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup/login/', authviews.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', authviews.LogoutView.as_view(), name='logout'),
    path('products/<int:id>/', views.productDetails , name='productDetails'),
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
    path('order/details/<slug:id>' , views.orderdetails ,name='user-detail'),
    path('ajax/wishlist' , views.updateWishlist.as_view(), name='wishlist-update'),
    path('ajax/wishlist/product/remove' , views.removeWishlist.as_view(), name='wishlist-remove'),
    path('wishlist', views.wishlist , name='wishlist'),
    path('Shop/<slug:pk>' , views.shop , name='shop'),
    path('Category/<slug:pk>' , views.smartphones , name='smartphones'),
    path('ajax/order/delete' , views.orderdelete.as_view() , name='orderDelete'),
    path('reset_password/', authviews.PasswordResetView.as_view(template_name="password/password_reset.html"), name="password_reset"),
    path('reset_password_sent/', authviews.PasswordResetDoneView.as_view(template_name="password/password_reset_done.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', authviews.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name="password_reset_confirm"),
    path('reset_password_complete', authviews.PasswordResetCompleteView.as_view(template_name="password/password_reset_complete.html"), name="password_reset_complete"),
    
    

]
#   +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns= urlpatterns + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
    urlpatterns= urlpatterns + static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)