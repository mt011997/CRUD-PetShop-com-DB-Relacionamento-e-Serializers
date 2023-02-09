from rest_framework import serializers


class TraitsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    trait_name = serializers.CharField(source="name", max_lenght=20)
    created_at = serializers.DateField(read_only=True)
