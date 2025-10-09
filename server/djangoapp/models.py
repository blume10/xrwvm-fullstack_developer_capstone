from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    founded = models.IntegerField(null=True, blank=True, help_text="Year founded (optional)")
    country = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Car Make"
        verbose_name_plural = "Car Makes"
        ordering = ['name']

    def __str__(self):
        return self.name

class CarModel(models.Model):
    # choices for body type
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    TRUCK = 'truck'
    COUPE = 'coupe'
    BODY_TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (TRUCK, 'Truck'),
        (COUPE, 'Coupe'),
    ]

    make = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE,
        related_name='models'
    )
    dealer_id = models.IntegerField(null=True, blank=True, help_text="External dealer id (Cloudant/Mongo)")
    name = models.CharField(max_length=100)
    body_type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES, default=SEDAN)
    # Year validators: minimum 2015, maximum 2023 as requested
    year = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(2015), MaxValueValidator(2023)],
        help_text="Year of the model (2015-2023)"
    )
    color = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Car Model"
        verbose_name_plural = "Car Models"
        ordering = ['-year', 'make', 'name']

    def __str__(self):
        y = f" ({self.year})" if self.year else ""
        return f"{self.make.name} {self.name}{y}"
