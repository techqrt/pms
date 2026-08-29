from django.db import models

class BuildingPhotos(models.Model):
    building_photos_id = models.AutoField(
        verbose_name='Building Photo Id',
        primary_key=True
    )
    building = models.ForeignKey(
        'property.Building',
        on_delete=models.CASCADE,
        related_name='photos'
    )
    photo = models.ImageField(
        verbose_name='Building Photo',
        upload_to='building_photos/',
        max_length=500,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "building_photos"
        ordering = ["-created_at"]
        verbose_name = "Building Photo"
        verbose_name_plural = "Building Photos"

    def __str__(self):
        return f"Photo {self.building_photos_id} for Building {self.building_id}"
