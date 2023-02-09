from rest_framework import serializers
from groups.serializer import GroupsSerializer
from traits.serializer import TraitsSerializer

from .models import SexChoise


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=SexChoise.choices,
        default=SexChoise.DEFAULT
    )
    group = GroupsSerializer()
    traits = TraitsSerializer(many=True)
