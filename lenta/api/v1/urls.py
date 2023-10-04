from django.urls import path, include, re_path

from api.v1 import views
from api.v1.views import SaveFilterTemplateView, ExportSelectedForecastsToExcelView

urlpatterns = [
	# path('user/', include('djoser.urls')),
	path('shops/', views.ShopsView.as_view(), name='shops-list'),
	path('categories/', views.CategoriesView.as_view(), name='categories-list'),
	path('sales/', views.SalesView.as_view(), name='sales-list'),
	path('export_selected_forecasts/',
		 ExportSelectedForecastsToExcelView.as_view(),
		 name='export_selected_forecasts'),
	path('forecast/', views.SalesForecastView.as_view(), name='forecast-list'),
	path('save-filter-template/', SaveFilterTemplateView.as_view(), name='save_filter_template'),

]
