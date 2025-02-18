from django.urls import path
from . import views

urlpatterns = [
    path('igp/', views.igp_report_view, name='igp_report_view'),
    path('igp-report-filter-pdf/', views.igp_report_filter_csv, name='igp_report_filter_csv'),
    path('igp-report-filter-csv/', views.igp_report_filter_pdf, name='igp_report_filter_pdf'),
    path('igp/export/csv/', views.export_igp_csv, name='export_igp_csv'),
    path('igp/export/pdf/', views.export_igp_pdf, name='export_igp_pdf'),
    path('ogp/export/csv/', views.export_ogp_csv, name='export_ogp_csv'),
    path('ogp/export/pdf/', views.export_ogp_pdf, name='export_ogp_pdf'),
]
