from django.urls import path, include, re_path


from api.v1 import views


urlpatterns = [

    # path('user/', include('djoser.urls')),
	path('shops/', views.ShopsView.as_view(), name='shops-list'),
	path('categories/', views.CategoriesView.as_view(), name='categories-list'),
	path('sales/', views.SalesView.as_view(), name='sales-list'),
	path('forecast/', views.SalesForecastView.as_view(), name='forecast-list'),

]