from django.urls import path

from django.conf.urls.static import static
from myproject import settings
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.start_page, name='start-page'),
    path('user-login', views.user_login, name='user-login'),
    path('add-order', views.add_order, name='add-order'),
    path('user-register', views.user_register, name='user-register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-car', views.add_car, name='add-car'),
    path('logout/', views.logout_user, name='logout'),
    path('list-orders', views.list_orders, name='list-orders'),
    path('answer-to-orders', views.answer_to_orders, name='answer-to-orders'),
    path('add-car-confirm', views.add_car_confirm, name='add-car-confirm'),
    path('add-order-confirm', views.add_order_confirm, name='add-order-confirm'),
    path('about', views.about, name='about'),
    path('orders/<int:order_id>/', views.order_detail, name='order-detail'),
    path('service', views.service, name='service'),
    path('tuning', views.tuning, name='tuning'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)