from django.urls import path

from core.reports.views import ReportSaleView
from core.reports.views import ReportRemitoView
urlpatterns = [
    # reports
    path('sale/', ReportSaleView.as_view(), name='sale_report'),
     path('remitos/', ReportRemitoView.as_view(), name='remito_report'),
]