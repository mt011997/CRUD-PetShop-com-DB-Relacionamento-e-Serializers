from django.db import models



class Trait(models.Model):
    name = models.CharField(max_length=20, unique=True)

    pets = models.ManyToManyField(
        "pets.Pet",
        related_name="traits"
    )

    def __repr__(self) -> str:
        return f'<[{self.id}] {self.name} - {self.fifa_code}>'
