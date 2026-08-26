from django.contrib import admin
from pms_apps.property.models.building import Building
from pms_apps.property.models.property import Property
from pms_apps.property.models.property_details import PropertyDetail
# Register your models here.


admin.site.register(Building)
admin.site.register(Property)
admin.site.register(PropertyDetail)