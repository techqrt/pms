from django.db import models

class PropertyPhotos(models.Model):
    property_photos_id = models.AutoField(
        verbose_name='Property Photo Id',
        primary_key=True
    )
    property = models.ForeignKey(
        'property.Property',
        on_delete=models.CASCADE,
        related_name='photos'
    )
    photo = models.URLField(
        verbose_name='Property Photo URL',
        max_length=500
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "property_photos"
        ordering = ["-created_at"]
        verbose_name = "Property Photo"
        verbose_name_plural = "Property Photos"

    def __str__(self):
        return f"Photo {self.property_photos_id} for Property {self.property_id}"