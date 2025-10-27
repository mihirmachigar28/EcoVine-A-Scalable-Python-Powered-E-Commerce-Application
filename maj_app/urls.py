from django.urls import path , include
from maj_app import views as v 
urlpatterns = [
path("", v.home,name='index'),
path('login',v.user_login, name="login"),
path('register',v.user_register, name='register'),
path('logout',v.user_logout, name='logout'),
path('product_details/<pid>', v.product_details, name="product_details"),
path('addtocart/<int:pid>', v.addtocart, name="addtocart"),
path('cart' , v.cart_view , name='cart'),
path('updateqty/<qv>/<cid>',v.updateqty , name ='updateqty'),
path('removepc/<cid>',v.removepc ,name = 'removepc'),
path('pay',v.pay,name="pay"),
path('placeorder',v.placeorder,name="place_order"),
path('add_to_saved/<int:pid>', v.add_to_saved, name='add_to_saved'),
path('saved', v.view_saved, name='saved'),

path('contactus/', v.contactus, name='contactus'),
]