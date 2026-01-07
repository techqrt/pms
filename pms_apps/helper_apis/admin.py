from django.contrib import admin

from pms_apps.helper_apis.models.city import City
from pms_apps.helper_apis.models.country import Country
from pms_apps.helper_apis.models.nationality import Nationality

admin.site.register(City)
admin.site.register(Country)
admin.site.register(Nationality)