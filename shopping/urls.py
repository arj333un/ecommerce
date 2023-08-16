from django.urls import path
from .import views


urlpatterns = [
   path('',views.index,name='index'),
   path('loginpage',views.loginpage,name='loginpage'),
   path('signup',views.signup,name='signup'),
   path('login_check',views.login_check,name='login_check'),
   path('admin_home',views.admin_home,name='admin_home'),
   path('user_home',views.user_home,name='user_home'),
   path('user_signup',views.user_signup,name='user_signup'),
   path('addcategory',views.addcategory,name='addcategory'),
   path('add_category',views.add_category,name='add_category'),
   path('addproduct',views.addproduct,name='addproduct'),
   path('proadd',views.proadd,name='proadd'),
   path('showprdct',views.showprdct,name='showprdct'),
   path('logout',views.logout,name='logout'),
   path('delete/<int:pk>',views.delete,name='delete'),
   path('user_details',views.user_details,name='user_details'),
   path('delete_user/<int:pk>',views.delete_user,name='delete_user'),
   path('categorized_products/<int:category_id>/',views.categorized_products,name='categorized_products'),
   path('cart',views.cart,name='cart'),
    path('cart_details/<int:pk>',views.cart_details,name='cart_details'),
   path('removecart/<int:pk>',views.removecart,name='removecart')

]