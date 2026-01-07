from django.urls import path
from pms_apps.helper_apis.controllers.city import CityViewController
from pms_apps.helper_apis.controllers.country import CountryViewController
from pms_apps.helper_apis.controllers.nationality import NationalityController

urlpatterns = [
    path('country/get_all',CountryViewController.get_all,name="get_all_countires"),
    path('city/get_all',CityViewController.get_all,name="get_all_cities"),
    path('nationality/get_all',NationalityController.get_all,name='get_all_nationalities')
]