from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from core import views as core_views

urlpatterns = [
    # path('admin/', admin.site.urls),

    # App URLs
    path('sales/', core_views.sales_view, name='sales'),
    path('sales/<int:sale_id>/receipt/', core_views.sale_receipt_view, name='sale_receipt'),

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('', core_views.products_view, name='products'),
    path('products/add/', core_views.product_create_edit_view, name='product_add'),
    path('products/<int:pk>/edit/', core_views.product_create_edit_view, name='product_edit'),
    path('products/<int:pk>/delete/', core_views.product_delete_view, name='product_delete'),
    
    path('sales/new/', core_views.new_sale_view, name='new_sale'),
    path('sales/report/', core_views.sales_report_view, name='sales_report'),
    # Tailwind
    # path("tailwind/", include("tailwind.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)