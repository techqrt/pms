from django.db import models
from django.db.models import Q

class Country(models.Model):
    country_id = models.AutoField(
        verbose_name='Country ID',
        primary_key=True
        )

    name = models.CharField(
        verbose_name='Country Name',
        max_length=25
    )

    @staticmethod
    def get(
        country_id : int
        ) -> dict:
        country = Country.objects.filter(country_id=country_id).values(
            "country_id","name"
        ).first()
        return country
    
    @staticmethod
    def get_all(
        search_key : str = ''
        ) -> list:
        countries = Country.objects.values(
            "country_id","name"
        )
        if search_key:
            countries = countries.filter(name__icontains=search_key)
        return countries


    def __str__(self):
        return str(self.name)
    
    class Meta:
        db_table = 'country'

