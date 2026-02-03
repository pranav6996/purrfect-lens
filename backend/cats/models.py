from django.db import models

class CatBreed(models.Model):
    name = models.CharField(max_length=100, unique=True)
    origin = models.CharField(max_length=100)
    description = models.TextField()
    health_info = models.TextField(help_text="Common health issues and life expectancy")
    habits = models.TextField(help_text="Behavioral traits and temperament")
    food_recommendations = models.TextField(help_text="Dietary needs and recommendations")
    
    def __str__(self):
        return self.name
