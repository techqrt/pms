from django.db import models

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
    def get(country_id : str):
        return Country.objects.filter(country_id=country_id).values(
            "country_id","name"
        ).first()

    def __str__(self):
        return str(self.name)
    
    class Meta:
        db_table = 'country'