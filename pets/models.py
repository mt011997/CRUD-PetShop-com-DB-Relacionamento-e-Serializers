from django.db import models


class SexChoise(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"
    DEFAULT = "Not Informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=20, choices=SexChoise.choices, default=SexChoise.DEFAULT
    )
    group = models.ForeignKey(
        "groups.Group", on_delete=models.PROTECT, related_name="pets", null=True
    )

    def __repr__(self) -> str:
        return f'<[{self.id}] {self.name} - {self.age}>'
