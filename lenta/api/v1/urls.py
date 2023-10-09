from django.urls import path, include

from api.v1.views import (
	SaveFilterTemplateView,
	ExportSelectedForecastsToExcelView,
	SalesForecastView,
	SalesView,
	CategoriesView,
	ShopsView,
	InfoHeaderView
)

urlpatterns = [
	# path('user/', include('djoser.urls')),
	path('shops/', ShopsView.as_view(), name='shops-list'),
	path('categories/', CategoriesView.as_view(), name='categories-list'),
	path('sales/', SalesView.as_view(), name='sales-list'),
	path('export_selected_forecasts/',
		 ExportSelectedForecastsToExcelView.as_view(),
		 name='export_selected_forecasts'),
	path('forecast/', SalesForecastView.as_view(), name='forecast-list'),
	path('save-filter-template/', SaveFilterTemplateView.as_view(), name='save_filter_template'),
	path('info-header/', InfoHeaderView.as_view(), name='info_header'),
]
