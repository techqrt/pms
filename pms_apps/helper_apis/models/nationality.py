from django.db import models

class Nationality(models.Model):
    nationality_id = models.AutoField(
        verbose_name='Nationality Id',
        primary_key=True
    )

    name = models.CharField(
        verbose_name='Nationality Name',
        max_length=25
    )

    @staticmethod
    def get(
        nationality_id : int
        ) -> dict:
        nationality = Nationality.objects.filter(nationality_id=nationality_id).values(
            "nationality_id","name"
        ).first()
        return nationality
    
    @staticmethod
    def get_all(
        search_key : str = ''
        ) -> list:
        nationality = Nationality.objects.values(
             "nationality_id","name"
        )
        if search_key:
            nationality = nationality.filter(name__icontains=search_key)

        return nationality


    def __str__(self):
        return str(self.name)
    
    class Meta:
        db_table = 'nationality'
