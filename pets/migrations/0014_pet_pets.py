# Generated by Django 4.0.5 on 2023-02-09 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0013_remove_pet_pets'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='pets',
            field=models.ManyToManyField(related_name='traits', to='pets.pet'),
        ),
    ]
