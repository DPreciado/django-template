from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
# Model for animals
class Animals(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    
    DIET_CHOICES = (
        ('MT', 'Meat'),
        ('PL', 'Plant'),
        ('OM', 'Omnivores'),
    )
    
    
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    diet = models.CharField(max_length=3, choices=DIET_CHOICES, )
    
    class Meta:
        db_table = 'animals'
        verbose_name = 'Animal'
        verbose_name_plural = 'Animals'
    