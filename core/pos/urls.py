from django.urls import path
from core.pos.views.category.views import *
from core.pos.views.provider.views import *
from core.pos.views.client.views import *
from core.pos.views.company.views import CompanyUpdateView
from core.pos.views.dashboard.views import *
from core.pos.views.product.views import *
from core.pos.views.sale.views import *
from core.pos.views.remitos.views import *
from core.pos.views.project.views import *


urlpatterns = [
    # dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # category
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    
    # provider
    path('provider/', ProviderListView.as_view(), name='provider_list'),
    path('provider/add/', ProviderCreateView.as_view(), name='provider_create'),
    path('provider/update/<int:pk>/', ProviderUpdateView.as_view(), name='provider_update'),
    path('provider/delete/<int:pk>/', ProviderDeleteView.as_view(), name='provider_delete'),

    # client
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/add/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    # product
    path('product/', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    # sale
    path('sale/', SaleListView.as_view(), name='sale_list'),
    path('sale/add/', SaleCreateView.as_view(), name='sale_create'),
    path('sale/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
    path('sale/update/<int:pk>/', SaleUpdateView.as_view(), name='sale_update'),
    path('sale/invoice/pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='sale_invoice_pdf'),
    # company
    path('company/update/', CompanyUpdateView.as_view(), name='company_update'),

    # remitos
    path('remitos/', RemitoListView.as_view(), name='remitos_list'),
    path('remitos/add/', RemitoCreateView.as_view(), name='remitos_create'),
    path('remitos/delete/<int:pk>/',RemitoDeleteView.as_view(), name='remitos_delete'),
    path('remitos/update/<int:pk>/', RemitoUpdateView.as_view(), name='remitos_update'),
    path('remitos/invoice/pdf/<int:pk>/', RemitoInvoicePdfView.as_view(), name='remitos_invoice_pdf'),
    
    #Proyectos
    path('project/', ProjectListView.as_view(), name='project_list'),
    path('project/add/', ProjectListView.as_view(), name='project_create'),
    path('project/update/<int:pk>/', ProjectUpdateView.as_view(), name='project_update'),
    path('project/delete/<int:pk>/', ProjectDeleteView.as_view(), name='project_delete'),
]
