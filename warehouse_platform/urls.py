from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("item/<int:item_id>", views.item, name="item"),
    path('add_item/', views.add_item, name='add_item'),
    path('', views.item_list, name='item_list'),
    path('item/<int:item_id>/edit/', views.edit_item, name='edit_item'),
    path('item/<int:item_id>/delete/', views.delete_item, name='delete_item'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('item/<int:item_id>/rent/', views.rent_item, name='rent_item'),
    path('manage_my_rentals/', views.manage_my_rentals, name='manage_my_rentals'),
    path('manage_my_listings/', views.manage_my_listings, name='manage_my_listings'),

]
# urls.py

