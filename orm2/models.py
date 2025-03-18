from django.db import models

# Create your models here.

class Business(models.Model):
    id = models.AutoField(primary_key=True) 
    name=models.CharField(max_length=255)
    revenue=models.FloatField(default=0.0)
    profit=models.FloatField(default=0.0)
    employees=models.IntegerField()
    country=models.CharField(max_length=255)

    class Meta:
        db_table = 'business' 

