from django.db import models
from pms_apps.helper_apis.models.country import Country
from django.db.models import Q

class City(models.Model):
    city_id = models.AutoField(
        verbose_name='City Id',
        primary_key=True
    )

    name = models.CharField(
        verbose_name='Country Name',
        max_length=25
    )

    country = models.ForeignKey(
        verbose_name="Country",
        to=Country,
        on_delete=models.CASCADE
    )

    @staticmethod
    def get(
        city_id : int
        ) -> dict:
        city = City.objects.filter(city_id=city_id).values(
            "city_id","name","country__name"
        ).first()
        return city
    
    @staticmethod
    def get_all(
        search_key : str = '',
        filter_key : str = '',
        filter_value : str = '',
        ) -> list:
        cities = City.objects.values(
            "city_id","name","country__name",
        )
        if filter_key and filter_value:
            cities = City.objects.filter(**{filter_key:filter_value})
        if search_key:
            cities = cities.filter(
                Q(name__icontains = search_key) |
                Q(country__name__icontains = search_key)
            )
        return cities
    
    def __str__(self):
        return str(self.name)
    
    class Meta:
        db_table = 'city'

